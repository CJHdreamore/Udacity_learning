############  SINEX Format ##########################
# 1. each line is at most 80 ASCII char

# 2. the first char of each lin represents the type of this line:
#        Type1:  % the first line and the last line
#        Type2:  * annotation
#        Type3:  + the start mark of a chunk
#        Type4:  - the end mark of a chunk
#        Type5:  <space> just data

# 3. SINEX contains 4 part : FILE/Reference;
#                           Input(Tropo description)
#                           STA ( Tropo STA_cordinates)
#                           Solution

# 4. STAX STAY STAZ : m

# 5.TROTOT: wet + dry Tropo delay    mm
#   TRODRY: dry tropo delay
#   TROWET: wet tropo delay
#   TGNTOT: tropo gradient in north (wet + dry)   mm
#   TGETOT: tropo gradient in east (wet + dry)  mm