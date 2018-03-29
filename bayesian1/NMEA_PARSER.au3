;~ nmea
#include<array.au3>
#include<file.au3>

$sData = "100NtTwP00JVkTPFit5irww@2>`<"
_ArrayDisplay(_NMEA_Position_Decoder($sData) , $sData)



Func _NMEA_Position_Decoder($sEncString)

$aAsc = StringToASCIIArray($sData)  ; any ASCII over 119 is invalid , ascii 64-87 and 88-95 are not used

for $i = 0 to ubound($aAsc) - 1
	If $aAsc[$i] < 48 Then
		msgbox(0, $aAsc[$i] , $aAsc[$i] & " asc less than 48" & @LF & chrw($aAsc[$i]) & " is not a valid char" )
		exit
	EndIF
	If $aAsc[$i] > 88 And $aAsc[$i] < 95 Then
		msgbox(0, $aAsc[$i] , $aAsc[$i] & " asc in invalid range 88-95")
		exit
	EndIF
	If $aAsc[$i] > 119 Then
		msgbox(0, $aAsc[$i] , $aAsc[$i] & " asc above 119")
		exit
	EndIF
next

;~ _ArrayDisplay($aAsc , 'ASCII values') ;check ASCII conversion
;subtract 48 from each

for $i = 0 to ubound($aAsc) - 1
	$aAsc[$i] = number($aAsc[$i] - 48)
	$aAsc[$i] = $aAsc[$i] > 40 ? $aAsc[$i] - 8 : $aAsc[$i] ; if still over 40 subtract 8
Next

;~ _ArrayDisplay($aAsc, 'armored payload') ;check armored payload

for $i = 0 to UBound($aAsc) - 1

	If $aAsc[$i] = "0" Then $aAsc[$i] = "000000"
	If $aAsc[$i] = "1" Then $aAsc[$i] = "000001"
	If $aAsc[$i] = "2" Then $aAsc[$i] = "000010"
	If $aAsc[$i] = "3" Then $aAsc[$i] = "000011"
	If $aAsc[$i] = "4" Then $aAsc[$i] = "000100"
	If $aAsc[$i] = "5" Then $aAsc[$i] = "000101"
	If $aAsc[$i] = "6" Then $aAsc[$i] = "000110"
	If $aAsc[$i] = "7" Then $aAsc[$i] = "000111"
	If $aAsc[$i] = "8" Then $aAsc[$i] = "001000"
	If $aAsc[$i] = "9" Then $aAsc[$i] = "001001"
	If $aAsc[$i] = "10" Then $aAsc[$i] = "001010"
	If $aAsc[$i] = "11" Then $aAsc[$i] = "001011"
	If $aAsc[$i] = "12" Then $aAsc[$i] = "001100"
	If $aAsc[$i] = "13" Then $aAsc[$i] = "001101"
	If $aAsc[$i] = "14" Then $aAsc[$i] = "001110"
	If $aAsc[$i] = "15" Then $aAsc[$i] = "001111"
	If $aAsc[$i] = "16" Then $aAsc[$i] = "010000"
	If $aAsc[$i] = "17" Then $aAsc[$i] = "010001"
	If $aAsc[$i] = "18" Then $aAsc[$i] = "010010"
	If $aAsc[$i] = "19" Then $aAsc[$i] = "010011"
	If $aAsc[$i] = "20" Then $aAsc[$i] = "010100"
	If $aAsc[$i] = "21" Then $aAsc[$i] = "010101"
	If $aAsc[$i] = "22" Then $aAsc[$i] = "010110"
	If $aAsc[$i] = "23" Then $aAsc[$i] = "010111"
	If $aAsc[$i] = "24" Then $aAsc[$i] = "011000"
	If $aAsc[$i] = "25" Then $aAsc[$i] = "011001"
	If $aAsc[$i] = "26" Then $aAsc[$i] = "011010"
	If $aAsc[$i] = "27" Then $aAsc[$i] = "011011"
	If $aAsc[$i] = "28" Then $aAsc[$i] = "011100"
	If $aAsc[$i] = "29" Then $aAsc[$i] = "011101"
	If $aAsc[$i] = "30" Then $aAsc[$i] = "011110"
	If $aAsc[$i] = "31" Then $aAsc[$i] = "011111"
	If $aAsc[$i] = "32" Then $aAsc[$i] = "100000"
	If $aAsc[$i] = "33" Then $aAsc[$i] = "100001"
	If $aAsc[$i] = "34" Then $aAsc[$i] = "100010"
	If $aAsc[$i] = "35" Then $aAsc[$i] = "100011"
	If $aAsc[$i] = "36" Then $aAsc[$i] = "100100"
	If $aAsc[$i] = "37" Then $aAsc[$i] = "100101"
	If $aAsc[$i] = "38" Then $aAsc[$i] = "100110"
	If $aAsc[$i] = "39" Then $aAsc[$i] = "100111"
	If $aAsc[$i] = "40" Then $aAsc[$i] = "101000"
	If $aAsc[$i] = "41" Then $aAsc[$i] = "101001"
	If $aAsc[$i] = "42" Then $aAsc[$i] = "101010"
	If $aAsc[$i] = "43" Then $aAsc[$i] = "101011"
	If $aAsc[$i] = "44" Then $aAsc[$i] = "101100"
	If $aAsc[$i] = "45" Then $aAsc[$i] = "101101"
	If $aAsc[$i] = "46" Then $aAsc[$i] = "101110"
	If $aAsc[$i] = "47" Then $aAsc[$i] = "101111"
	If $aAsc[$i] = "48" Then $aAsc[$i] = "110000"
	If $aAsc[$i] = "49" Then $aAsc[$i] = "110001"
	If $aAsc[$i] = "50" Then $aAsc[$i] = "110010"
	If $aAsc[$i] = "51" Then $aAsc[$i] = "110011"
	If $aAsc[$i] = "52" Then $aAsc[$i] = "110100"
	If $aAsc[$i] = "53" Then $aAsc[$i] = "110101"
	If $aAsc[$i] = "54" Then $aAsc[$i] = "110110"
	If $aAsc[$i] = "55" Then $aAsc[$i] = "110111"
	If $aAsc[$i] = "56" Then $aAsc[$i] = "111000"
	If $aAsc[$i] = "57" Then $aAsc[$i] = "111001"
	If $aAsc[$i] = "58" Then $aAsc[$i] = "111010"
	If $aAsc[$i] = "59" Then $aAsc[$i] = "111001"
	If $aAsc[$i] = "60" Then $aAsc[$i] = "111100"
	If $aAsc[$i] = "61" Then $aAsc[$i] = "111101"
	If $aAsc[$i] = "62" Then $aAsc[$i] = "111110"
	If $aAsc[$i] = "63" Then $aAsc[$i] = "111111"

next

;~ _ArrayDisplay($aAsc , 'bitstream') ;check bit stream

$sBitStream = _ArrayToString($aAsc , "")

$sMsgType = stringleft($sBitStream , 6)
$sRptIndicator = stringmid($sBitStream , 7 , 2)
$sMMSI = StringMid($sBitStream , 9 , 30)
$sNavStatus   = StringMid($sBitStream , 39 , 4)
$sRateOfTurn = StringMid($sBitStream , 43 , 8)
$sSpeedOverGrnd = StringMid($sBitStream , 51 , 10)
$sPositionAccuracy = StringMid($sBitStream , 61 , 1)
$slongitude = StringMid($sBitStream , 62 , 28)
$slatitude = StringMid($sBitStream , 90 , 27)
$sCourseOverGround = StringMid($sBitStream , 117 , 12)
$sHeading = StringMid($sBitStream , 129 , 9)
$sTimeStamp = StringMid($sBitStream , 138 , 6)
$sManeuverIndicator = StringMid($sBitStream , 144 , 2)
$sSpare = StringMid($sBitStream , 146 , 3) ;unused
$sRAIMflag = StringMid($sBitStream , 149 , 1)
$sRadioStatus = StringMid($sBitStream , 150 , 19) ;ending at 168 (or 28 blocks of 6)

;~ local $aBitStream[1][2] = [["message" , $sMsgType]]

local $aBitStream[16][2] = [["msg_type" , _BinaryToDec($sMsgType)] , ["Repeat Ind" , _BinaryToDec($sRptIndicator)] , ["MMSI" , _BinaryToDec($sMMSI)] , ["Nav Status" , _BinaryToDec($sNavStatus)] , ["Turn Rate" , _BinaryToDec($sRateOfTurn) / 10] , _
["Speed" , _BinaryToDec($sSpeedOverGrnd) / 10] , ["Accuracy" , _BinaryToDec($sPositionAccuracy)] , ["longitude" , $slongitude] , ["latitude" , $slatitude], ["Course" , _BinaryToDec($sCourseOverGround) / 10] , ["Heading" , _BinaryToDec($sHeading)] , ["TimeStamp" , _BinaryToDec($sTimeStamp)] , _
["Maneuver Ind" , _BinaryToDec($sManeuverIndicator)] , ["Spare" , $sSpare] , ["RAIM flag" , _BinaryToDec($sRAIMflag)] , ["Radio Status" , _BinaryToDec($sRadioStatus)]]

Return $aBitStream

EndFunc ;NMEA Position Decoder



;~ ;-------------Binary To Dec-----------------


Func _BinaryToDec($strBin)
Local $Return
Local $lngResult
Local $intIndex

	If StringRegExp($strBin,'[0-1]') then
	$lngResult = 0
	For $intIndex = StringLen($strBin) to 1 step -1
	$strDigit = StringMid($strBin, $intIndex, 1)
	Select
	case $strDigit="0"
	; do nothing
	case $strDigit="1"
	$lngResult = $lngResult + (2 ^ (StringLen($strBin)-$intIndex))
	case else
	; invalid binary digit, so the whole thing is invalid
	$lngResult = 0
	$intIndex = 0 ; stop the loop
	EndSelect
	Next

	$Return = $lngResult
		Return $Return
	Else
		MsgBox(0,"Error","Wrong input, try again ...")
		Return
	EndIf
EndFunc
