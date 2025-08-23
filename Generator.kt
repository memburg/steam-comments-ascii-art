import java.awt.Color
import java.awt.image.BufferedImage
import java.io.File
import javax.imageio.ImageIO

val COMMENT_WIDTH = 25
val COMMENT_HEIGHT = 13
val FINAL_WIDTH = 2 * COMMENT_WIDTH
val FINAL_HEIGHT = 4 * COMMENT_HEIGHT
val PROPORTION = FINAL_WIDTH.toDouble() / FINAL_HEIGHT
val BRAILLE_SIZE = 192
val BRAILLE_CHARACTERS = (
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

fun threshold(
    image: BufferedImage,
    theta: Int,
) {
    for (x in 0 until image.width) {
        for (y in 0 until image.height) {
            val rgb = image.getRGB(x, y)
            val color = Color(rgb)
            val avg = (color.red + color.green + color.blue) / 3
            if (avg < theta) {
                image.setRGB(x, y, Color(0, 0, 0).rgb)
            } else {
                image.setRGB(x, y, Color(255, 255, 255).rgb)
            }
        }
    }
}

fun resize(image: BufferedImage): BufferedImage {
    val scaled = BufferedImage(FINAL_WIDTH, FINAL_HEIGHT, BufferedImage.TYPE_INT_RGB)
    val g = scaled.createGraphics()
    g.drawImage(image, 0, 0, FINAL_WIDTH, FINAL_HEIGHT, null)
    g.dispose()
    return scaled
}

fun crop(image: BufferedImage): BufferedImage {
    val width = image.width
    val height = image.height
    val newWidth = (height * PROPORTION).toInt()
    val toCentre = (width - newWidth) / 2
    return image.getSubimage(toCentre, 0, newWidth, height)
}

fun extractSubimage(
    image: BufferedImage,
    x: Int,
    y: Int,
): BufferedImage = image.getSubimage(x, y, 2, 4)

fun getAsciiCharacter(subimage: BufferedImage): Char {
    // This is a stub: in the Python code, you compare to reference images.
    // Here, we use a simple heuristic: count black pixels.
    var count = 0
    for (x in 0 until 2) {
        for (y in 0 until 4) {
            val rgb = subimage.getRGB(x, y)
            val color = Color(rgb)
            if (color.red < 128) count++
        }
    }
    // Map count to a braille character index (0..191)
    val idx = (count * BRAILLE_SIZE / 8).coerceIn(0, BRAILLE_SIZE - 1)
    return BRAILLE_CHARACTERS[idx]
}

fun getAsciiImage(image: BufferedImage): List<List<Char>> {
    val asciiImage = mutableListOf<List<Char>>()
    for (y in 0 until image.height step 4) {
        val row = mutableListOf<Char>()
        for (x in 0 until image.width step 2) {
            val subimage = extractSubimage(image, x, y)
            row.add(getAsciiCharacter(subimage))
        }
        asciiImage.add(row)
    }
    return asciiImage
}

fun printAscii(ascii: List<List<Char>>) {
    for (row in ascii) {
        println(row.joinToString(""))
    }
}

fun main(args: Array<String>) {
    if (args.isEmpty()) {
        println("Usage: kotlin Generator.kt <image_path> [--t threshold] [--o output]")
        return
    }
    val imagePath = args[0]
    var thresholdValue = 100
    var outputName = "ascii.png"
    for (i in 1 until args.size) {
        when (args[i]) {
            "--t" -> if (i + 1 < args.size) thresholdValue = args[i + 1].toInt()
        }
    }
    val image = ImageIO.read(File(imagePath))
    val cropped = crop(image)
    val resized = resize(cropped)
    threshold(resized, thresholdValue)
    ImageIO.write(resized, "png", File(outputName))
    val asciiArray = getAsciiImage(resized)
    printAscii(asciiArray)
}
