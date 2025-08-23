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
    val toCentre = ((width - newWidth) / 2)
    return image.getSubimage(toCentre, 0, newWidth, height)
}

fun extractSubimage(
    image: BufferedImage,
    x: Int,
    y: Int,
): BufferedImage = image.getSubimage(x, y, 2, 4)

fun getBrailleImages(): List<String> =
    File("braille")
        .listFiles()
        ?.filter { it.isFile && it.name.endsWith(".png") && it.name != ".DS_Store" }
        ?.map { it.name }
        ?: emptyList()

fun getAsciiCharacter(subimage: BufferedImage): Char {
    val brailleImages = getBrailleImages()
    var closestMatch = ""
    val subPixels = Array(2) { Array(4) { 0 } }
    for (x in 0 until 2) {
        for (y in 0 until 4) {
            val rgb = subimage.getRGB(x, y)
            subPixels[x][y] = if (Color(rgb).red < 128) 0 else 255
        }
    }
    for (asciiImage in brailleImages) {
        val idx = asciiImage.substring(8, 11).toIntOrNull() ?: continue
        val braille = ImageIO.read(File("braille/$asciiImage"))
        var matches = 0
        for (x in 0 until 2) {
            for (y in 0 until 4) {
                val bRgb = braille.getRGB(x, y)
                val bVal = if (Color(bRgb).red < 128) 0 else 255
                if (bVal == subPixels[x][y]) matches++
            }
        }
        if (matches == 8) return BRAILLE_CHARACTERS[idx]
        if (matches == 7) closestMatch = BRAILLE_CHARACTERS[idx].toString()
    }
    return if (closestMatch.isNotEmpty()) closestMatch[0] else ' '
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

fun printAscii(a: List<List<Char>>) {
    for (r in a) {
        println(r.joinToString(""))
    }
}

fun main(args: Array<String>) {
    if (args.isEmpty()) {
        println("Usage: kotlin Generator.kt <image_path> [--t threshold] [--o output]")
        return
    }
    var thresholdValue = 100
    var outputName = "ascii.png"
    var imagePath = args[0]
    for (i in 1 until args.size) {
        when (args[i]) {
            "--t" -> if (i + 1 < args.size) thresholdValue = args[i + 1].toInt()
            "--o" -> if (i + 1 < args.size) outputName = args[i + 1]
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
