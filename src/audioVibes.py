from pedalboard import Pedalboard, Reverb, LowpassFilter, Gain
from pedalboard.io import AudioFile
import subprocess
import sys
import getopt
import os

class AudioVibes:
   def __init__(self, argv):
      self.sample_rate = 48000.0
      self.arg_input = ""
      self.arg_output = ""
      self.arg_vibe = ""
      self.arg_remove = False
      self.arg_help = "USAGE: {0} -i <input> -v <vibe> [-o <output>] [-r]".format(argv[0])
      self.parse_args(argv)
      self.main()

   def parse_args(self, argv):
      # Get the command line arguments
      try:
         opts, args = getopt.getopt(argv[1:], "hri:o:v:", ["help", "remove-raw", "input=", "output=", "vibe="])
      except:
         print(self.arg_help)
         sys.exit(2)

      # Process the command line arguments
      for opt, arg in opts:
         if opt in ("-h", "--help"):
            print(self.arg_help)  # print the help message
            sys.exit(2)
         elif opt in ("-i", "--input"):
            self.arg_input = arg
         elif opt in ("-o", "--output"):
            self.arg_output = arg
         elif opt in ("-v", "--vibe"):
            self.arg_vibe = arg
         elif opt in ("-r", "--remove-raw"):
            self.arg_remove = True

      # Check if output file ends with mp3
      if self.arg_output != "" and self.arg_output[-4:] != ".mp3":
         print("Output file must end with .mp3")
         sys.exit(2)

      # Check if the input is a youtube video
      if self.arg_input.startswith("https://www.youtube.com/"):
         print("Input is a youtube video")
      else:
         if not os.path.isfile(self.arg_input):
            print("Input file does not exist")
            sys.exit(2)
         else:
            print("Input is a local file")


      # Check if vibe is set
      if self.arg_vibe == "":
         print("Vibe is not set")
         sys.exit(2)

      # Check if vibe is valid
      if self.arg_vibe not in ("bathroom_at_club", "bathroom_at_party"):
         print("Vibe is not valid")
         sys.exit(2)
      
   def load_audio(self):
      # Check if the source is youtube
      if self.arg_input.startswith("https://www.youtube.com/"):
         print("Downloading audio from youtube")
         youtube_command = ['youtube-dl', '-o', '%(title)s.%(ext)s', '-x', '--audio-format', 'mp3', '--audio-quality', '0', self.arg_input]

         p = subprocess.Popen(youtube_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
         for line in p.stdout:
            line = line.decode("utf-8").rstrip()
            print(line)
            if line[0:len('[ffmpeg] Destination: ')] == '[ffmpeg] Destination: ' and line[-3:] == 'mp3':
               self.audio_file = line[len('[ffmpeg] Destination: '):]
         p.wait()
         print("Download complete")
      # If the source is a file
      else:
         self.audio_file = self.arg_input

      # Load the audio file
      print("Opening audio file: {0}".format(self.audio_file))
      with AudioFile(self.audio_file).resampled_to(self.sample_rate) as f:
         self.audio = f.read(f.frames)

   def apply_vibe(self):
      print("Setting vibe: {0}".format(self.arg_vibe))
      # Apply the bathroom at party vibe
      if self.arg_vibe == "bathroom_at_club":
         board = Pedalboard([
            Reverb(room_size=0.5, damping=0.25, wet_level=0.4, dry_level=0.6, width=0.5) # Club accoustics
            , LowpassFilter(cutoff_frequency_hz=150) # Sound bleeding through the walls
            , Reverb(room_size=0.2, damping=0.1, wet_level=0.2, dry_level=0.8, width=0.2) # Bathroom accoustics
            , Gain(gain_db=-6) # Assume signal to be too hot, ideally this would be corrected based on actual average peak
         ])

         self.vibe_description = " but you're in the bathroom at a club"

      elif self.arg_vibe == "bathroom_at_party":
         board = Pedalboard([
            Reverb(room_size=0.3, damping=0.3, wet_level=0.4, dry_level=0.6, width=0.3) # Party accoustics
            , LowpassFilter(cutoff_frequency_hz=250) # Sound bleeding through the walls
            , Reverb(room_size=0.15, damping=0.2, wet_level=0.2, dry_level=0.8, width=0.2) # Bathroom accoustics
            , Gain(gain_db=-6) # Assume signal to be too hot, ideally this would be corrected based on actual average peak
         ])

         self.vibe_description = " but you're in the bathroom at a party"
         
      print("Applying vibe")
      # Run the audio through the effects chain
      self.audio_processed = board(self.audio, self.sample_rate)
      
   def save_audio(self):
      print("Saving audio")
      if self.arg_output != "":
         self.output_path = self.arg_output
      else:
         self.output_path = self.audio_file[:len(self.audio_file)-4] + self.vibe_description + '.mp3'
      # Write the audio as a mp3 file:

      with AudioFile(self.output_path, 'w', self.sample_rate, self.audio_processed.shape[0]) as f:
         f.write(self.audio_processed)

   def remove_raw_audio(self):
      # Remove the raw audio file if the option is specified
      if self.arg_remove:
         print("Removing raw audio")
         os.remove(self.audio_file)

   def main(self):
      self.load_audio()
      self.apply_vibe()
      self.save_audio()
      self.remove_raw_audio()

      print("Done! Check out {0}".format(self.output_path))
      return 0
      