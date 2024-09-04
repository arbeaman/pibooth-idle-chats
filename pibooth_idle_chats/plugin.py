import os
import os.path as osp
import glob
import time
import shutil
import pygame
import pibooth

from pathlib import Path
from pibooth.utils import LOGGER

@pibooth.hookimpl
def pibooth_startup(app, cfg):
    # Require pibooth-sound-effects
    # Should not need to init the mixer again
    """Init the pygame mixer and load available chats"""
    
    print( "PiBooth startup in pibooth idle chats" )

    pygame.mixer.pre_init(channels=2, buffer=1024)
    pygame.mixer.init()

    one_second_bytes_length = 4 * 44100

    # Init List of chat files
    chat_path = cfg.getpath('IDLECHATS', 'chat_path')

    app.chat_index = 0
    app.idle_start = time.perf_counter()
    app.chats = {}

    # Get list of all .wav files, with full paths in the folder pointed to by the config line IDLECHATS:chat_path
    # Sort the files by name
    chat_file_list = sorted( filter( os.path.isfile, glob.glob(chat_path + '/*.wav') ) )

    # Process each file found
    #   Check if it is a .wav
    #       if so, get the full path to the file and load the file with pygame.mixer.Sound
    #       into the chats list, with a numeric index based on sort order
    for idx, chat in enumerate(chat_file_list):
        print( "Loading sound #", idx, " file '", chat, "'" )
        app.chats[idx] = pygame.mixer.Sound(file=chat)
        print( "File loaded. ", app.chats[idx].get_length(), " bytes" )

@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
    print( "PiBooth configure in pibooth idle chats" )

    cfg.add_option('IDLECHATS', 'chat_path', "~/.config/pibooth/chats",
                   "Path to the chat folder")

    cfg.add_option('IDLECHATS', 'chat_delay', 
                   # 60*1.5,
                   15,
                   "Time between idle chats")

@pibooth.hookimpl
def state_wait_enter(app):
    """Reset the chat index"""
    print( "PiBooth wait enter in pibooth idle chats" )
    app.idle_start = time.perf_counter()
    app.chat_index = 0

@pibooth.hookimpl
def state_wait_do(app, cfg):
    """Check how much time has elapsed"""
    now_time = time.perf_counter()
    delta_time = now_time - app.idle_start
    chat_str_delay = cfg.get('IDLECHATS', 'chat_delay')

    try:
        chat_delay=float(chat_str_delay)
    except Exception:
        print( "[ERROR] Exception converting ", chat_str_delay, " to a float, defaulting to 90." )
        chat_delay = 90

    # print( "Chat delay is ", chat_delay, " in state_wait_do. Delta_time is ", delta_time )
    if delta_time > float(chat_delay):
        # print( "Delta time is ", delta_time, " from start of ", app.idle_start )
        # print( "Speaking chat #", app.chat_index, ". ", app.chats[app.chat_index].get_length(), " bytes long.  At volume ", app.chats[app.chat_index].get_volume() )

        # Speak the chat
        app.chats[app.chat_index].play()

        # Restart the timer
        app.idle_start = time.perf_counter()

        #print( "Idle start changed to ", app.idle_start )

        # Go to the next chat (wrapping)
        app.chat_index = (app.chat_index + 1) % len(app.chats)
    
@pibooth.hookimpl
def pibooth_reset(cfg, hard):
    """Populate chat folder if it doesn't exists"""
    print( "PiBooth reset in pibooth idle chats" )

    chat_path = cfg.getpath('IDLECHATS', 'chat_path')
    #source_chat_path = osp.join(osp.dirname(osp.abspath(__file__)), 'chats')
    source_chat_path = osp.join(osp.dirname(Path(__file__).parent.absolute()), 'chats')
    print( "Copying chat files from ", source_chat_path)

    # On a hard reset, remove the installed chats directory
    if hard and osp.isdir(chat_path):
        shutil.rmtree(chat_path, ignore_errors=True)

    # If the .config chats directory does not exist, create and populate it
    if not osp.isdir(chat_path):
        # source_chat_path = osp.join(osp.dirname(osp.abspath(__file__)), 'chats')
        LOGGER.info("Generate chats directory in '%s'", chat_path)
        shutil.copytree(source_chat_path, chat_path)

