
import ffmpeg

def convert_audio(input_file, output_file):
    try:
        input_stream = ffmpeg.input(input_file)
        output_stream = ffmpeg.output(input_stream, output_file)

        # Run the conversion and capture the result
        ffmpeg.run(output_stream)
        return {
            "success": True
        }
    except ffmpeg.Error as e:
        return {
            "success": False,
            "msg": f"Error during conversion: {e.stderr}"
        } 