#!/bin/bash


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
   SFILE=$( ~/talk/photochat.sh -w "${NUM}" )

   # Convert the talk wave file to one in chats with the proper name

   # Get the desired name
   printf -v FILE "photochat%02d.wav" "${NUM}"

   ## 2-photochat00.wav
   ## Find the most recent file with that name (the name can be preceeded with 1-, 2-, etc.)
   #echo "Searching for '~/talk/wav/*${FILE}'"
   #ls -1r ~/talk/wav/*${FILE}
   #SFILE=`ls -1r ~/talk/wav/*${FILE} | head -1`

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

