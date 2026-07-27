COMMENT_WIDTH = 25
COMMENT_HEIGHT = 13
FINAL_WIDTH = 2 * COMMENT_WIDTH
FINAL_HEIGHT = 4 * COMMENT_HEIGHT
PROPORTION = FINAL_WIDTH.to_f / FINAL_HEIGHT
BRAILLE_CHARACTERS = (
  "⡀⡁⡂⡃⡄⡅⡆⡇⡈⡉⡊⡋⡌⡍⡎⡏" +
  "⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛⡜⡝⡞⡟" +
  "⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯" +
  "⡰⡱⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿" +
  "⢀⢁⢂⢃⢄⢅⢆⢇⢈⢉⢊⢋⢌⢍⢎⢏" +
  "⢐⢑⢒⢓⢔⢕⢖⢗⢘⢙⢚⢛⢜⢝⢞⢟" +
  "⢠⢡⢢⢣⢤⢥⢦⢧⢨⢩⢪⢫⢬⢭⢮⢯" +
  "⢰⢱⢲⢳⢴⢵⢶⢷⢸⢹⢺⢻⢼⢽⢾⢿" +
  "⣀⣁⣂⣃⣄⣅⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏" +
  "⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟" +
  "⣠⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯" +
  "⣰⣱⣲⣳⣴⣵⣶⣷⣸⣹⣺⣻⣼⣽⣾⣿"
)

def threshold(image, theta)
  (0...image.width).each do |x|
    (0...image.height).each do |y|
      rgb = image.get_rgb(x, y)
      color = java.awt.Color.new(rgb)
      avg = (color.red + color.green + color.blue) / 3
      if avg < theta
        image.set_rgb(x, y, java.awt.Color.new(0, 0, 0).rgb)
      else
        image.set_rgb(x, y, java.awt.Color.new(255, 255, 255).rgb)
      end
    end
  end
end

def resize(image)
  scaled = java.awt.image.BufferedImage.new(FINAL_WIDTH, FINAL_HEIGHT, java.awt.image.BufferedImage::TYPE_INT_RGB)
  g = scaled.create_graphics
  g.set_rendering_hint(java.awt.RenderingHints::KEY_INTERPOLATION, java.awt.RenderingHints::VALUE_INTERPOLATION_BICUBIC)
  g.set_rendering_hint(java.awt.RenderingHints::KEY_RENDERING, java.awt.RenderingHints::VALUE_RENDER_QUALITY)
  g.draw_image(image, 0, 0, FINAL_WIDTH, FINAL_HEIGHT, nil)
  g.dispose
  scaled
end

def crop(image)
  width = image.width
  height = image.height
  new_width_f = height * PROPORTION
  to_centre = ((width - new_width_f) / 2).to_i
  new_width = new_width_f.to_i
  sub = image.get_subimage(to_centre, 0, new_width, height)
  result = java.awt.image.BufferedImage.new(new_width, height, java.awt.image.BufferedImage::TYPE_INT_RGB)
  g = result.create_graphics
  g.draw_image(sub, 0, 0, nil)
  g.dispose
  result
end

def extract_subimage(image, x, y)
  image.get_subimage(x, y, 2, 4)
end

def braille_images
  Dir.children("braille").select { |f| f.end_with?(".png") && f != ".DS_Store" }
end

def ascii_character(subimage)
  images = braille_images
  closest = ""
  sub_pixels = Array.new(2) { Array.new(4, 0) }
  (0...2).each do |x|
    (0...4).each do |y|
      rgb = subimage.get_rgb(x, y)
      sub_pixels[x][y] = java.awt.Color.new(rgb).red < 128 ? 0 : 255
    end
  end
  images.each do |name|
    idx = name[8, 3].to_i rescue nil
    next unless idx
    braille = javax.imageio.ImageIO.read(java.io.File.new("braille/#{name}"))
    matches = 0
    (0...2).each do |x|
      (0...4).each do |y|
        b_rgb = braille.get_rgb(x, y)
        b_val = java.awt.Color.new(b_rgb).red < 128 ? 0 : 255
        matches += 1 if b_val == sub_pixels[x][y]
      end
    end
    return BRAILLE_CHARACTERS[idx] if matches == 8
    closest = BRAILLE_CHARACTERS[idx] if matches == 7
  end
  closest.empty? ? " " : closest
end

def ascii_image(image)
  result = []
  (0...image.height).step(4) do |y|
    row = []
    (0...image.width).step(2) do |x|
      sub = extract_subimage(image, x, y)
      row << ascii_character(sub)
    end
    result << row
  end
  result
end

def print_ascii(a)
  a.each { |row| puts row.join("") }
end

if __FILE__ == $0
  if ARGV.empty?
    puts "Usage: jruby generator.rb <image> [--t threshold]"
    exit
  end
  threshold_value = 100
  i = 0
  image_path = nil
  while i < ARGV.size
    case ARGV[i]
    when "--t"
      threshold_value = ARGV[i + 1].to_i if ARGV[i + 1]
      i += 1
    else
      image_path ||= ARGV[i] unless ARGV[i].start_with?("--")
    end
    i += 1
  end
  image = javax.imageio.ImageIO.read(java.io.File.new(image_path))
  cropped = crop(image)
  resized = resize(cropped)
  threshold(resized, threshold_value)
  ascii_arr = ascii_image(resized)
  print_ascii(ascii_arr)
end
