# Steam Comments Braille ASCII Art Generator
#
# Converts an image into a 25×13 grid of Unicode Braille characters
# suitable for Steam profile comments. Each Braille character encodes
# a 2×4 pixel block (8 dots → 8 bits → one Unicode codepoint).
#
# Usage: jruby generator.rb <image> [--t threshold]

# Steam comment grid dimensions (characters).
COMMENT_WIDTH = 25
COMMENT_HEIGHT = 13

# Pixel dimensions. Each Braille cell covers a 2×4 pixel area:
#   2 pixels wide × 4 pixels tall.
FINAL_WIDTH = 2 * COMMENT_WIDTH
FINAL_HEIGHT = 4 * COMMENT_HEIGHT

# Target aspect ratio used by the crop step to centre the source image.
PROPORTION = FINAL_WIDTH.to_f / FINAL_HEIGHT

# Binarizes the image in place: pixels below the threshold become
# black (0, 0, 0), pixels at or above become white (255, 255, 255).
#
# Lower threshold → darker output (fewer white pixels → fewer dots).
# Higher threshold → lighter output (more white pixels → more dots).
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

# Scales the image to FINAL_WIDTH × FINAL_HEIGHT pixels using
# bicubic interpolation for smooth results.
def resize(image)
  scaled = java.awt.image.BufferedImage.new(FINAL_WIDTH, FINAL_HEIGHT, java.awt.image.BufferedImage::TYPE_INT_RGB)
  g = scaled.create_graphics
  g.set_rendering_hint(java.awt.RenderingHints::KEY_INTERPOLATION, java.awt.RenderingHints::VALUE_INTERPOLATION_BICUBIC)
  g.set_rendering_hint(java.awt.RenderingHints::KEY_RENDERING, java.awt.RenderingHints::VALUE_RENDER_QUALITY)
  g.draw_image(image, 0, 0, FINAL_WIDTH, FINAL_HEIGHT, nil)
  g.dispose
  scaled
end

# Crops the source image to the target aspect ratio by trimming
# equal amounts from the left and right edges (horizontal centre
# crop). Returns a copy independent of the source image buffer.
def crop(image)
  new_width_f = image.height * PROPORTION
  to_centre = ((image.width - new_width_f) / 2).to_i
  new_width = new_width_f.to_i
  sub = image.get_subimage(to_centre, 0, new_width, image.height)
  result = java.awt.image.BufferedImage.new(new_width, image.height, java.awt.image.BufferedImage::TYPE_INT_RGB)
  g = result.create_graphics
  g.draw_image(sub, 0, 0, nil)
  g.dispose
  result
end

# Extracts a single 2×4 pixel block from the image at logical
# Braille-cell coordinates (x, y) in pixels.
def extract_subimage(image, x, y)
  image.get_subimage(x, y, 2, 4)
end

# Maps a 2×4 thresholded pixel block to its Unicode Braille character.
#
# Pixel-to-dot mapping (standard Unicode Braille block U+2800-U+28FF):
#   (0,0) → dot 1 (bit 0)    (1,0) → dot 4 (bit 3)
#   (0,1) → dot 2 (bit 1)    (1,1) → dot 5 (bit 4)
#   (0,2) → dot 3 (bit 2)    (1,2) → dot 6 (bit 5)
#   (0,3) → dot 7 (bit 6)    (1,3) → dot 8 (bit 7)
#
# A white pixel (red >= 128) means the dot is raised ("on").
# The resulting 8-bit mask is added to the Braille base codepoint
# U+2800 to produce the character.
def ascii_character(subimage)
  code = 0
  [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [0, 3], [1, 3]].each_with_index do |(x, y), bit|
    code |= (1 << bit) if java.awt.Color.new(subimage.get_rgb(x, y)).red >= 128
  end
  (0x2800 + code).chr("UTF-8")
end

# Converts a full thresholded image into a 2D array of Braille
# characters, one per 2×4 pixel block.
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

# Prints a 2D array of Braille characters, one row per line.
def print_ascii(a)
  a.each { |row| puts row.join("") }
end

# ── Entry point ──────────────────────────────────────────────────

if __FILE__ == $0
  if ARGV.empty?
    puts "Usage: jruby generator.rb <image> [--t threshold]"
    exit
  end

  threshold_value = 100
  image_path = ARGV.find { |a| !a.start_with?("--") }
  t_index = ARGV.index("--t")
  threshold_value = ARGV[t_index + 1].to_i if t_index && ARGV[t_index + 1]

  image = javax.imageio.ImageIO.read(java.io.File.new(image_path))
  cropped = crop(image)
  resized = resize(cropped)
  threshold(resized, threshold_value)
  ascii_arr = ascii_image(resized)
  print_ascii(ascii_arr)
end
