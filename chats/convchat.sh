#!/bin/bash

# The prerequisites of this script are not included in this repository.
# Instead of running this script, use the .wav files included in the chats directory.

# This script creates the chat wav files and moves them to the chats directory.
# It uses another script that was designed to run in the background to do the chats.  That script is no longer needed with this plugin.
echo "WARNING: This script converts the output of an old photochat script to the wav files used by this pluging."
echo "The photochat script is not included and is not needed since the output is provided in the chats directory."
echo "This script will fail without the photochats script that is not publically available."
echo " Press Control-C to exit"
read X

cd ~/pibooth-idle-chats/chats/
rm ~/pibooth-idle-chats/chats/*.wav
rm ~/talk/wav/*-photochat*.wav

NUMCHATS="$( ~/talk/photochat.sh -n )"
echo "We have '${NUMCHATS}' chat messages"

for ((NUM=0; NUM<NUMCHATS; NUM++))
do
   # Create the .wav file in ~/talk/wav
   # Do a single chat at a time so there is no delay
   echo "Creating photochat #'${NUM}'"
   # Get the name of the wav file photochat produced
   SFILE=$( ~/talk/photochat.sh -w "${NUM}" )

   # Convert the talk wave file to one in chats with the proper name

   # Get the desired name
   printf -v FILE "photochat%02d.wav" "${NUM}"

   if ! [ -f "${SFILE}" ]
   then
     echo "ERROR: File #${NUM}, '${SFILE}' does not exist"
     exit 1
   fi

   echo "Converting '${SFILE}' to '${FILE}'"

   # Convert the file type and name
   #  Amplify the volume, convert to 2 channels, and make it 44.1 kHz
   ffmpeg -i "${SFILE}" -filter:a "volume=1.5" -sample_fmt s16 -ar 44100 -ac 2 "${FILE}"

   echo "Playing '${FILE}'"
   aplay "${FILE}"
done

