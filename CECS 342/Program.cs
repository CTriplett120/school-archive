
static string FormatByteSize(long byteSize)
{
    string[] sizes = {"B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB"};
    string deci = "00"; // stores previous number's decimal values for display
    
    // goes through all sizes included in array
    for (int i = 0; i < sizes.Length; i++)
    {
        // if bytesize has reached the correct range of 0 - 999
        if (byteSize < 1000)
        {
            string tempstr = byteSize.ToString();
            // adds decimal rounding if these aren't in Bytes
            if (i != 0)
            {
                tempstr += '.' + deci;
            }
            return  tempstr + sizes[i];
        }
        // if bytesize isn't in the proper range yet
        else
        {
            deci = byteSize.ToString(); // store value in deci
            
            // preserves only the values we want (what our next decimal values will be)
            deci = deci.Substring((deci.Length % 4) + 1, 2);
            
            byteSize /= 1000;
            
        }
        
    }
    
    // file is bigger than 1000 ZB
    return "> 1000 ZB";

}
