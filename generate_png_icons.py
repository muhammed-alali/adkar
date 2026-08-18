import zlib, struct

def make_png(width, height, color_bg, color_fg):
    # RGB values
    br, bg, bb = color_bg
    fr, fg, fb = color_fg
    
    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0) # filter byte 0
        for x in range(width):
            # draw a rounded square & crescent placeholder
            dx = x - width / 2
            dy = y - height / 2
            dist = (dx*dx + dy*dy) ** 0.5
            
            # Inner circle/star design
            if (dist < width * 0.35 and dist > width * 0.22 and (dx > -width*0.1 or dy < 0)) or (dist < width*0.1):
                raw_data.extend([fr, fg, fb])
            elif abs(dx) < width*0.42 and abs(dy) < height*0.42:
                raw_data.extend([br, bg, bb])
            else:
                raw_data.extend([br//2, bg//2, bb//2])
                
    def chunk(two_type, data):
        return struct.pack('>I', len(data)) + two_type + data + struct.pack('>I', zlib.crc32(two_type + data) & 0xffffffff)

    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(raw_data, 9))
    png += chunk(b'IEND', b'')
    return png

# Generate 192x192 and 512x512
with open('icon-192.png', 'wb') as f:
    f.write(make_png(192, 192, (15, 138, 95), (197, 155, 39)))

with open('icon-512.png', 'wb') as f:
    f.write(make_png(512, 512, (15, 138, 95), (197, 155, 39)))

print("PNG icons created successfully!")
