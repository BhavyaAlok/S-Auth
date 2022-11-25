import java.lang.reflect.UndeclaredThrowableException;
import java.security.GeneralSecurityException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.math.BigInteger;
import java.util.TimeZone;
import java.util.concurrent.TimeUnit;
 
class TOTP {
 
   private TOTP() {}
 
    private static byte[] hmac_sha(String crypto, byte[] keyBytes, byte[] text){
        try{
           Mac hmac;
           hmac = Mac.getInstance(crypto);
           SecretKeySpec macKey = new SecretKeySpec(keyBytes, "RAW");
           hmac.init(macKey);
           return hmac.doFinal(text);
        }
        catch(GeneralSecurityException gse){
           throw new UndeclaredThrowableException(gse);
        }
   }
 
   private static byte[] hexStr2Bytes(String hex){
       // Adding one byte to get the right conversion
       // Values starting with "0" can be converted
       byte[] bArray = new BigInteger("10" + hex,16).toByteArray();
 
       // Copy all the REAL bytes, not the "first"
       byte[] ret = new byte[bArray.length - 1];
       for(int i = 0; i < ret.length; i++)
           ret[i] = bArray[i+1];
       return ret;
   }
 
   private static final int[] DIGITS_POWER = {1,10,100,1000,10000,100000,1000000,10000000,100000000 };
 
   public static String generateTOTP(String key,
           String time,
           String returnDigits){
       return generateTOTP(key, time, returnDigits, "HmacSHA1");
   }
 
   public static String generateTOTP256(String key,
           String time,
           String returnDigits){
       return generateTOTP(key, time, returnDigits, "HmacSHA256");
   }
 
   public static String generateTOTP512(String key,
           String time,
           String returnDigits){
       return generateTOTP(key, time, returnDigits, "HmacSHA512");
   }
 
   public static String generateTOTP(String key,
           String time,
           String returnDigits,
           String crypto){
       int codeDigits = Integer.decode(returnDigits).intValue();
       String result = null;
 
       while (time.length() < 16 )
           time = "0" + time;
 
       // Get the HEX in a Byte[]
       byte[] msg = hexStr2Bytes(time);
       byte[] k = hexStr2Bytes(key);
 
       byte[] hash = hmac_sha(crypto, k, msg);
 
       // put selected bytes into result int
       int offset = hash[hash.length - 1] & 0xf;
 
       int binary =
           ((hash[offset] & 0x7f) << 24) |
           ((hash[offset + 1] & 0xff) << 16) |
           ((hash[offset + 2] & 0xff) << 8) |
           (hash[offset + 3] & 0xff);
 
       int otp = binary % DIGITS_POWER[codeDigits];
 
       result = Integer.toString(otp);
       while (result.length() < codeDigits) {
           result = "0" + result;
       }
       return result;
   }
 
   public static void main(String[] args) {
        // String seed64 = "3132333435363738393031323334353637383930" +
        // "3132333435363738393031323334353637383930" +
        // "3132333435363738393031323334353637383930" +
        // "31323334";
        String seed64 = args[0];
        long T0 = 0;
        long X = 30;
        String steps = "0";
        long T = (System.currentTimeMillis()/1000);
        T = T/X;    
        steps = Long.toHexString(T).toUpperCase();
        while (steps.length() < 16) steps = "0" + steps;
        String otp = generateTOTP(seed64, steps, "6", "HmacSHA512");
        System.out.println(otp);
   }
}