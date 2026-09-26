import struct, sys, os, datetime, glob
PID={0x22:'VLP-16',0x28:'VLP-32C',0xa1:'VLS-128',0x21:'HDL-32E'}
RM={0x37:'strongest',0x38:'last',0x39:'dual'}
for p in sys.argv[1:]:
    with open(p,'rb') as f:
        gh=f.read(24); magic=struct.unpack('<I',gh[:4])[0]
        n=0; first=last=None; ports={}; modes={}; pids={}; sizes={}
        while True:
            h=f.read(16)
            if len(h)<16: break
            ts,us,incl,orig=struct.unpack('<IIII',h)
            d=f.read(incl)
            if first is None: first=ts+us/1e6
            last=ts+us/1e6; n+=1
            if len(d)>=42:
                dport=struct.unpack('>H',d[36:38])[0]; pl=d[42:]
                ports[dport]=ports.get(dport,0)+1
                sizes[len(pl)]=sizes.get(len(pl),0)+1
                if len(pl)==1206:
                    modes[pl[1204]]=modes.get(pl[1204],0)+1; pids[pl[1205]]=pids.get(pl[1205],0)+1
    fmt=lambda d,m=None:{(m.get(k,hex(k)) if m else k):v for k,v in sorted(d.items(),key=lambda x:-x[1])[:3]}
    print(f"{os.path.basename(p)} | {os.path.getsize(p)/1e6:.1f}MB | pkts={n} | {datetime.datetime.fromtimestamp(first).strftime('%Y-%m-%d %H:%M:%S')} | dur={last-first:.1f}s | ports={fmt(ports)} | model={fmt(pids,PID)} | mode={fmt(modes,RM)}")
