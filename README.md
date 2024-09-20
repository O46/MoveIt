Creator: o46

Purpose: Utilizes FTP to move completed P2P transfers via qBittorrent to a target network destination. Capable of moving single files, and entire directory trees.

Dependencies:
  Python 3.#
  qBittorrent
  
How to set up:
  qBittorrent
  -> Settings
    -> "Downloads"
      -> Enable "Run on torrent finished" 
      -> Enter this command: python "Full\Path\To\Script" -contentType "%L" -contentPath "%F"
  config.ini
    [db]
      -> server
        your server's IP address
      -> movie
        destination folder for movies
      -> tv
        destination folder for tv shows
      -> other
        destination folder for anything else
    [auth]
      -> user
        your username
      -> pass
        your password
  
Note: This script assumes you've defined the nature of the transfer (Movie,TV Show, etc.) If you haven't it will try to guess whether it's a movie or tv show, and defaults to "Other". Movie or TV Show is inferred using Firas Dib's regex https://regex101.com/library/yP4bY4

Warning: This script requires you to store your credentials locally in un-salted, unencrypted, insecure plaintext
Warning: Not for use with copyrighted materials

Final note: You're free to modify this, even distribute it if you like. In those circumstances, I would appreciate but do not require an acknowledgement.
