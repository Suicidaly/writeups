from nbtlib import nbt

def retouch_rev(nbt_file): 
    LIGHT_STEPS = [14, 7, 10, 3, 13, 6, 9, 12]
    
    nbt_data = nbt.load(nbt_file)
    
    entities = []
    for entity in nbt_data['entities']:
        if entity['nbt']['id'] == 'minecraft:armor_stand':
            bukkit_values = entity['nbt'].get('BukkitValues', {})
            rotation_keys = sorted([k for k in bukkit_values.keys() 
                                   if k.startswith('chickenjockeyfightclub:rotation_')])
            x, y, z = entity['pos']
            
            raw_segments = []
            for key in rotation_keys:
                byte_array = bukkit_values[key]
                raw_segments.append(byte_array)
            
            entities.append({
                'x': float(x), 'y': float(y), 'z': float(z),
                'raw': raw_segments
            })
    
    entities.sort(key=lambda e: (e['x'], e['z'], e['y']))
    
    data = b''.join([
        bytes([
            ((int(b) + 256 - LIGHT_STEPS[i % len(LIGHT_STEPS)]) % 256)
            for i, b in enumerate(seg)
        ])
        for entity in entities
        for seg in entity['raw']
    ])

    if data[:4] == b'\xca\xfe\xba\xbe':
        with open(f"decoded.class", "wb") as f:
            f.write(data)
        print(f"Saved as 'decoded.class'\n")


if __name__ == "__main__":
    nbt_file = r"./lobby.nbt"
    retouch_rev(nbt_file)