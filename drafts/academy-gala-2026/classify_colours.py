import numpy as np, json, sys
from PIL import Image
from skimage.color import rgb2lab
D=sys.argv[1]
FAM={"black":"#1A1A1A","white & cream":"#EFE8DA","grey & silver":"#A3A6AA","red":"#C8202A","pink":"#E889A6",
     "orange":"#E8743B","yellow & gold":"#D9B34A","beige & nude":"#CDB497","brown":"#6B4128","green":"#9DBE8F",
     "blue & teal":"#3F7F93","purple":"#7B3F99"}
VIS={k:tuple(int(v[i:i+2],16) for i in (1,3,5)) for k,v in FAM.items()}
VIS["skin/hair"]=(200,200,200)
def classify(lab):
    L,a,b=lab[...,0],lab[...,1],lab[...,2]; C=np.hypot(a,b); h=(np.degrees(np.arctan2(b,a))+360)%360
    out=np.full(L.shape,"",dtype=object)
    def s(mask,name):
        m=mask&(out=="" ); out[m]=name
    s((L<32)&(C<14),"black")
    s((L<12)&(C<22),"black")
    s((L>=78)&(C<8),"white & cream")
    s((L>=76)&(C<24)&(h>=60)&(h<100),"white & cream")
    s((C<8),"grey & silver")
    s((C>=8)&(h>=270)&(h<335),"purple")
    s((C>=8)&(h>=175)&(h<270),"blue & teal")
    s((C>=8)&(h>=100)&(h<175),"green")
    s((C<14),"grey & silver")
    s((h>=335)|(h<26),"pink")
    s((h>=26)&(h<44)&(C<35)&(L>=55),"pink")
    s((h>=26)&(h<44)&(C<35),"brown")
    s((h>=26)&(h<44)&(L>=26),"red")
    s((h>=26)&(h<44),"red")
    s((h>=44)&(h<75)&(L<40),"brown")
    s((h>=44)&(h<70)&(C>=48),"orange")
    s((h>=44)&(h<100)&(C<48)&(h<75),"beige & nude")
    s((h>=70)&(h<100),"yellow & gold")
    return out
res={}
for k in range(1,34):
    n=f"look-{k:02d}"
    a=np.array(Image.open(f"{D}/{n}_full.png").convert("RGBA")); bb=Image.fromarray(a).getbbox(); a=a[bb[1]:bb[3],bb[0]:bb[2]]
    m=a[...,3]>200; lab=rgb2lab(a[...,:3]/255.); H=a.shape[0]
    L,A,B=lab[...,0],lab[...,1],lab[...,2]
    # skin ref from face band
    band=np.zeros_like(m); band[int(.03*H):int(.09*H)]=True
    sk=m&band&(A>6)&(B>8)&(L>25)&(L<85)
    skin=np.median(lab[sk],0) if sk.sum()>50 else np.array([60,15,20])
    noskin=np.linalg.norm(lab-skin,axis=2)>=float(sys.argv[2])
    head=np.zeros_like(m); head[:int(.10*H)]=True
    C=np.hypot(A,B); hh=(np.degrees(np.arctan2(B,A))+360)%360
    skinlike=(hh>=40)&(hh<78)&(C>=14)&(C<=50)&(L>=28)&(L<=88)
    NUDE={"look-08","look-23"}
    if n in NUDE: skinlike=np.linalg.norm(lab-skin,axis=2)<12
    use=m&noskin&~head&~skinlike
    fam=classify(lab)
    OV={"look-02":{"black":"brown"},"look-14":{"grey & silver":"pink"},"look-27":{"brown":"red"}}
    for src,dst in OV.get(n,{}).items(): fam[fam==src]=dst
    if n=="look-09": fam[(fam=="black")&(hh>=175)&(hh<270)&(C>=3)]="blue & teal"
    if n=="look-32": use=use&(fam!="red")&(fam!="brown")
    if n in ("look-12","look-06"): use=use&(fam!="brown")
    tot=use.sum(); sh={f:float((use&(fam==f)).sum()/tot*100) for f in FAM}
    sh3={f:v for f,v in sorted(sh.items(),key=lambda x:-x[1])[:3] if v>=5}; t3=sum(sh3.values()); sh3={f:round(v/t3*100,1) for f,v in sh3.items()}
    res[n]={"top3":sh3,"skin":skin.round(1).tolist(),"shares":{f:round(v,1) for f,v in sorted(sh.items(),key=lambda x:-x[1]) if v>=0.5}}
    vis=np.full(a.shape[:2]+(3,),255,np.uint8); vis[m]=VIS["skin/hair"]
    for f in FAM: vis[use&(fam==f)]=VIS[f]
    Image.fromarray(vis).save(f"{D}/{n}_fam.png")
json.dump(res,open(f"{D}/fam.json","w"),indent=1)
for n,r in res.items(): print(n, r["top3"], "| all:", {k:v for k,v in r["shares"].items() if v>=3})
