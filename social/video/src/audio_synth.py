#!/usr/bin/env python3
"""The Cruise Lab launch batch — original synthesised soundtracks (no copyrighted material).
Usage: python3 audio_synth.py <l1|l2|l3|l4> <duration_s> <out.wav>
Music bed + beat-timed SFX per the launch-scripts audio specs. Stereo 44.1k.
"""
import sys, numpy as np
from scipy.signal import butter, lfilter
from scipy.io import wavfile

SR = 44100
rng = np.random.default_rng(7)

def zeros(dur): return np.zeros(int(SR*dur))
def tt(dur): return np.arange(int(SR*dur))/SR
def adsr(n, a, d, s, r, slevel=0.6):
    env = np.ones(n)*slevel
    A, D, R = int(a*SR), int(d*SR), int(r*SR)
    A=max(A,1); D=max(D,1); R=max(R,1)
    env[:A] = np.linspace(0,1,A)
    env[A:A+D] = np.linspace(1,slevel,min(D,max(0,n-A)))[:max(0,n-A)][:D] if n>A else env[A:A+D]
    if R < n: env[-R:] *= np.linspace(1,0,R)
    return env[:n]
def expdec(dur, k): t=tt(dur); return np.exp(-t*k)
def bp(x, lo, hi, order=2):
    b,a = butter(order, [lo/(SR/2), hi/(SR/2)], btype='band'); return lfilter(b,a,x)
def lp(x, fc, order=2):
    b,a = butter(order, fc/(SR/2)); return lfilter(b,a,x)
def hp(x, fc, order=2):
    b,a = butter(order, fc/(SR/2), btype='high'); return lfilter(b,a,x)

# ---------- instruments ----------
def sine(f, dur, k=0.0):
    t=tt(dur); ph=2*np.pi*(f*t + 0.5*k*t*t)  # optional linear sweep k Hz/s
    return np.sin(ph)
def kick(dur=0.35):
    t=tt(dur); f=120*np.exp(-t*22)+45
    return np.sin(2*np.pi*np.cumsum(f)/SR)*expdec(dur,14)
def hat(dur=0.06, open_=False):
    d = 0.18 if open_ else dur
    return hp(rng.standard_normal(int(SR*d)), 7000)*expdec(d, 28 if open_ else 90)*0.6
def snap(dur=0.09):
    return bp(rng.standard_normal(int(SR*dur)), 1500, 4500)*expdec(dur,60)
def bassnote(f, dur, drive=1.6):
    t=tt(dur); x=np.sin(2*np.pi*f*t)+0.4*np.sin(2*np.pi*2*f*t)
    x=np.tanh(x*drive); return lp(x,500)*adsr(len(x),0.005,0.05,0.7,0.08)
def pluck(f, dur=0.9):
    t=tt(dur)
    x=(np.sin(2*np.pi*f*t)+0.5*np.sin(2*np.pi*f*2.01*t)+0.25*np.sin(2*np.pi*f*3.0*t))
    return x*expdec(dur,5)
def pad(freqs, dur, cutoff=900, wob=0.15):
    t=tt(dur); x=np.zeros_like(t)
    for f in freqs:
        for det in (0.997,1.0,1.004):
            x+=np.sin(2*np.pi*f*det*t+rng.uniform(0,6))
    x=lp(x,cutoff)
    lfo=1+wob*np.sin(2*np.pi*0.4*t)
    n=len(x); e=np.ones(n); F=int(0.8*SR)
    e[:min(F,n)]=np.linspace(0,1,min(F,n)); e[-min(F,n):]*=np.linspace(1,0,min(F,n))
    return x*lfo*e/len(freqs)/3

# ---------- sfx ----------
def whoosh(dur=0.55, up=True):
    x=rng.standard_normal(int(SR*dur)); t=tt(dur)
    f0,f1=(300,3800) if up else (3800,300)
    out=np.zeros_like(x); steps=22
    for i in range(steps):
        a,b=int(i*len(x)/steps),int((i+1)*len(x)/steps)
        fc=f0+(f1-f0)*(i/steps)**1.6
        out[a:b]=bp(x, max(80,fc*0.6), min(16000,fc*1.5))[a:b]
    envl=np.sin(np.pi*t/dur)**1.5
    return out*envl
def stamp_thunk():
    dur=0.55; t=tt(dur)
    body=np.sin(2*np.pi*np.cumsum(95*np.exp(-t*16)+38)/SR)*expdec(dur,9)
    click=hp(rng.standard_normal(int(SR*0.03)),2500)*expdec(0.03,120)*0.9
    x=body*1.4; x[:len(click)]+=click
    boom=lp(rng.standard_normal(len(t)),140)*expdec(dur,7)*0.9
    return np.tanh(x+boom)
def tick():
    return hp(rng.standard_normal(int(SR*0.03)),3500)*expdec(0.03,150)*0.9
def receipt_tick():
    d=0.05
    a=bp(rng.standard_normal(int(SR*d)),2000,6000)*expdec(d,90)
    b=sine(1150,0.04)*expdec(0.04,90)*0.5
    x=a; x[:len(b)]+=b; return x
def chaching():
    d=1.1; t=tt(d)
    bell=lambda f,dl: np.concatenate([zeros(dl),(np.sin(2*np.pi*f*tt(d-dl))+0.6*np.sin(2*np.pi*f*2.76*tt(d-dl)))*expdec(d-dl,6)])
    x=bell(1318,0)+bell(1760,0.09)+0.7*bell(2217,0.16)
    shk=bp(rng.standard_normal(len(t)),4000,9000)*expdec(d,20)*0.5
    return (x*0.6+shk)
def buzzer():
    d=0.38; t=tt(d)
    sq=np.sign(np.sin(2*np.pi*138*t))*0.7+np.sign(np.sin(2*np.pi*207*t))*0.4
    am=0.6+0.4*np.sign(np.sin(2*np.pi*28*t))
    return lp(sq*am,2400)*adsr(len(t),0.004,0.05,0.85,0.06)
def riser(dur=1.4):
    t=tt(dur)
    x=bp(rng.standard_normal(len(t)),400,6000)
    sweep=np.sin(2*np.pi*np.cumsum(180*np.exp(t*2.2))/SR)*0.4
    e=(t/dur)**2.3
    return (x*0.8+sweep)*e
def wind_gust(dur=1.6, strength=1.0):
    t=tt(dur); x=lp(rng.standard_normal(len(t)),900)
    e=np.sin(np.pi*t/dur)**2*strength
    flut=1+0.35*np.sin(2*np.pi*7*t)*np.sin(2*np.pi*1.3*t)
    return x*e*flut
def sting_gold():
    d=2.2
    x=pluck(392,d)*0.8+pluck(494,d)*0.7+pluck(587,d)*0.6+pluck(784,d)*0.5
    x=np.concatenate([x[:int(0.0*SR)], x])[:int(d*SR)]
    shimmer=hp(rng.standard_normal(int(d*SR)),8000)*expdec(d,4)*0.15
    return lp(x,4000)+shimmer
def beatdrop_sub():
    d=0.8; t=tt(d)
    return np.sin(2*np.pi*np.cumsum(70*np.exp(-t*3)+35)/SR)*expdec(d,4)*1.3
def creak_swell(dur=2.6):
    t=tt(dur)
    f=180+40*np.sin(2*np.pi*0.7*t)
    x=np.sin(2*np.pi*np.cumsum(f)/SR)
    x=bp(x+0.5*rng.standard_normal(len(t)),120,700)
    e=np.sin(np.pi*t/dur)**1.5
    wash=lp(rng.standard_normal(len(t)),450)*e*0.7
    return (x*0.35+wash)*e

# ---------- mixer ----------
class Mix:
    def __init__(self, dur):
        self.n=int(SR*dur); self.L=np.zeros(self.n); self.R=np.zeros(self.n)
    def put(self, x, t, gain=1.0, pan=0.0):
        i=int(t*SR); j=min(self.n, i+len(x))
        if i>=self.n: return
        seg=x[:j-i]*gain
        self.L[i:j]+=seg*(1-max(0,pan)); self.R[i:j]+=seg*(1+min(0,pan))
    def duck(self, times, depth=0.5, dur=0.45):
        env=np.ones(self.n)
        for t0 in times:
            i=int(t0*SR); j=min(self.n,i+int(dur*SR))
            if i>=self.n: continue
            k=np.exp(-np.arange(j-i)/SR*9)
            env[i:j]*=1-depth*k
        return env

def bed_l1(dur):
    m=Mix(dur); bpm=122; beat=60/bpm
    roots=[73.42,65.41,69.30,73.42]  # D2 C2 C#2->use A? keep D C D# pattern minor-ish
    roots=[73.42,69.30,65.41,77.78]
    b=0.0; bar=0
    while b<dur:
        m.put(kick(),b,0.95); m.put(kick(),b+beat*1.75,0.45)
        m.put(snap(),b+beat*2,0.5)
        for h in range(8):
            m.put(hat(),b+h*beat/2+beat/4,0.22 if h%2 else 0.14)
        f=roots[bar%4]
        for q in [0,1.5,2,3,3.5]:
            m.put(bassnote(f,0.32),b+q*beat,0.5)
        b+=beat*4; bar+=1
    m.put(pad([146.8,174.6,220],min(dur,10),700),0,0.16)
    m.put(pad([130.8,155.6,196],10,650),10,0.16)
    return (m.L+m.R)/2
def bed_l2(dur):
    m=Mix(dur); bpm=116; beat=60/bpm
    roots=[82.41,82.41,77.78,73.42]  # E2 E2 Eb2 D2 sneaky chromatic
    b=0.0; bar=0
    while b<dur:
        m.put(kick(),b,0.9); m.put(kick(),b+beat*2.5,0.5)
        m.put(snap(),b+beat*1,0.45); m.put(snap(),b+beat*3,0.5)
        for h in range(4): m.put(hat(),b+h*beat+beat/2,0.25)
        f=roots[bar%4]
        for q in [0,0.75,2,2.75,3.5]:
            m.put(bassnote(f,0.22,1.9),b+q*beat,0.55)
        b+=beat*4; bar+=1
    m.put(pad([164.8,196,246.9],min(dur,12),620),0,0.12)
    return (m.L+m.R)/2
def bed_l3(dur):
    m=Mix(dur); bpm=120; beat=60/bpm
    chords=[[130.8,164.8,196],[110,138.6,164.8],[123.5,146.8,185],[130.8,164.8,196]]  # C Am Bm-ish C
    roots=[65.41,55,61.74,65.41]
    b=0.0; bar=0
    while b<dur:
        m.put(kick(),b,0.85); m.put(kick(),b+beat*2,0.7)
        m.put(snap(),b+beat*1,0.4); m.put(snap(),b+beat*3,0.45)
        for h in range(8): m.put(hat(),b+h*beat/2+beat/4,0.26 if h%2 else 0.16)
        f=roots[bar%4]
        for q in [0,1,1.5,2,3]:
            m.put(bassnote(f,0.28),b+q*beat,0.5)
        ch=chords[bar%4]
        m.put(pluck(ch[0]*2,0.5),b,0.18); m.put(pluck(ch[1]*2,0.5),b+beat*1.5,0.15)
        b+=beat*4; bar+=1
    m.put(pad([261.6,329.6,392],min(dur,14),900,0.1),0,0.10)
    return (m.L+m.R)/2
def bed_l4(dur, turn=3.2):
    m=Mix(dur)
    # warm airy opening
    m.put(pad([196,246.9,293.7,392],turn+0.6,1100,0.2),0,0.30)   # G major air
    m.put(pluck(784,1.4),0.4,0.12); m.put(pluck(587.3,1.4),1.5,0.10)
    # cold minor after the turn, sparse pulse
    bpm=100; beat=60/bpm; b=turn
    seg=dur-turn
    m.put(pad([174.6,207.7,261.6],seg,700,0.25),turn,0.22)       # F minor-ish chill
    m.put(pad([155.6,185,233.1],seg,650,0.25),turn+8,0.18)
    bar=0
    while b<dur:
        m.put(kick(),b,0.65)
        m.put(hat(),b+beat,0.16); m.put(hat(),b+beat*1.5,0.10)
        m.put(bassnote(43.65,0.5),b,0.45)   # F1
        b+=beat*2; bar+=1
    # constant light breeze under everything
    breeze=lp(rng.standard_normal(m.n),600)*0.10
    t=np.arange(m.n)/SR
    breeze*= (0.6+0.4*np.sin(2*np.pi*0.23*t))*np.where(t>turn,1.35,0.8)
    return (m.L+m.R)/2+breeze

def normalize(x, peak=0.89):
    mx=np.max(np.abs(x))+1e-9
    return x/mx*peak

def soft_ends(x, fade=0.12):
    n=len(x); F=int(fade*SR)
    x[:F]*=np.linspace(0,1,F); x[-F:]*=np.linspace(1,0,F)
    return x

def build(video, dur):
    m=Mix(dur)
    if video=='l1':
        bed=bed_l1(dur)
        hits=[0.06,0.42,1.05,2.05,3.25,6.05,9.05,12.05,16.15,17.8]
        bed*=m.duck(hits,0.55,0.5)
        m.put(bed,0,0.34)
        for t0 in [0.06,0.42,1.05]: m.put(tick(),t0,0.9)          # hook word punches
        m.put(stamp_thunk(),2.05,0.75)                             # #186 lands
        m.put(whoosh(0.6,True),3.05,0.8)                           # deck-plan zoom
        m.put(tick(),4.15,0.7)                                     # cabin card
        m.put(whoosh(0.4,False),6.0,0.55); m.put(tick(),6.12,0.8)  # reason 1
        m.put(whoosh(0.4,False),9.0,0.55); m.put(creak_swell(2.6),9.1,0.75)  # motion swell
        m.put(whoosh(0.4,False),12.0,0.55); m.put(tick(),12.12,0.8)
        m.put(riser(1.5),14.65,0.85)
        m.put(stamp_thunk(),16.15,1.15)                            # BAD CABIN
        m.put(sting_gold(),17.85,0.7)                              # end card
        m.put(tick(),18.35,0.5)
    elif video=='l2':
        bed=bed_l2(dur)
        item_ts=[2.6,5.2,7.8,10.4,13.0]
        hits=[0.06,0.5,*item_ts,16.0,19.3]
        bed*=m.duck(hits,0.5,0.4)
        m.put(bed,0,0.34)
        for t0 in [0.06,0.5,1.15]: m.put(tick(),t0,0.9)
        m.put(whoosh(0.5,True),2.25,0.6)
        for i,t0 in enumerate(item_ts):
            m.put(tick(),t0,0.8)
            m.put(buzzer(),t0+0.55,0.8)                            # CONFISCATED slap
            m.put(stamp_thunk(),t0+0.55,0.45)
        m.put(riser(1.2),15.0,0.7)
        m.put(tick(),16.05,0.9); m.put(tick(),17.2,0.7)
        m.put(sting_gold(),19.35,0.7)
    elif video=='l3':
        bed=bed_l3(dur)
        line_ts=[4.4,5.9,7.4,8.9,10.6]
        hits=[0.06,0.5,1.3,*line_ts,12.6,15.2,17.3,21.6,25.6]
        bed*=m.duck([12.6,15.2,25.6],0.5,0.5)
        m.put(bed,0,0.36)
        for t0 in [0.06,0.5,1.3]: m.put(tick(),t0,0.9)
        m.put(whoosh(0.5,True),3.35,0.6)
        for t0 in line_ts: m.put(receipt_tick(),t0,1.0)
        m.put(riser(1.1),11.6,0.8)
        m.put(chaching(),12.75,0.9)                                # £579
        m.put(beatdrop_sub(),15.25,1.0); m.put(tick(),15.25,0.9)   # £41/day twist
        m.put(tick(),17.35,0.8)                                    # honest beat
        m.put(whoosh(0.4,False),21.5,0.5); m.put(tick(),21.65,0.8) # sea vs port
        m.put(sting_gold(),25.7,0.7)
    elif video=='l4':
        bed=bed_l4(dur,turn=3.2)
        bed*=m.duck([3.2,6.6,9.6,12.6,15.7,19.7],0.45,0.5)
        m.put(bed,0,0.5)
        m.put(pluck(987.8,1.2),0.15,0.14)                          # golden sparkle
        m.put(tick(),0.1,0.6); m.put(tick(),0.9,0.5)
        m.put(wind_gust(1.8,1.1),3.0,0.9)                          # the turn
        m.put(whoosh(0.7,False),3.2,0.5)
        m.put(wind_gust(2.2,1.3),6.4,1.0); m.put(tick(),6.7,0.8)   # wind 74%
        m.put(tick(),9.7,0.8); m.put(wind_gust(1.6,0.8),9.6,0.7)   # 4 of 5 years
        m.put(tick(),12.7,0.8)                                     # warmth 34%
        m.put(stamp_thunk(),16.6,0.7)                              # WINDBREAKER
        m.put(wind_gust(1.8,0.9),15.6,0.7)
        m.put(sting_gold(),19.85,0.7)
    def master(ch):
        ch=normalize(ch,0.95)
        ch=np.tanh(ch*2.4)          # soft-knee drive: lifts the bed, rounds the peaks
        return soft_ends(normalize(ch,0.91))
    return np.stack([master(m.L),master(m.R)],axis=1)

if __name__=='__main__':
    video, dur, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
    x=build(video,dur)
    wavfile.write(out,(SR),(x*32767).astype(np.int16))
    print(f'{out}: {dur}s stereo')
