import pygame as pg, random as r, math as m
pg.init(); s=pg.display.set_mode((800,400)); c=pg.time.Clock(); f=pg.font.SysFont('Arial',18); sk,pi=0.9,m.pi
def rs():
 global b,t,pw,rn,gm,wn; t,pw,rn,gm,wn=1,0,True,0,""
 b=[[200.0,200.0,0.0,0.0,0,0,(255,255,255)]]
 ps=[(550,200),(572,189),(572,211),(594,178),(594,200),(594,222),(616,167),(616,189),(616,211),(616,233)]
 cl=[(255,215,0),(0,0,255),(255,0,0),(75,0,130),(255,140,0),(34,139,34),(139,0,0),(0,0,0),(255,105,180),(255,255,0)]
 for i in range(10): b.append([float(ps[i][0]),float(ps[i][1]),0.0,0.0,i+1,3 if i==7 else (1 if i<5 else 2),cl[i]])
rs()
while rn:
 s.fill((34,139,34)); pg.draw.rect(s,(139,69,19),(0,0,800,400),20); mv=any(m.hypot(l[2],l[3])>0.15 for l in b)
 for e in pg.event.get():
  if e.type==pg.QUIT: rn=False
  if e.type==pg.KEYDOWN:
   if e.key==pg.K_r or (gm and e.key==pg.K_y): rs()
   if gm and e.key==pg.K_n: rn=False
 if not gm:
  if not mv:
   if t==1:
    mx,my=pg.mouse.get_pos(); a=m.atan2(my-b[0][1],mx-b[0][0])
    if pg.mouse.get_pressed()[0]: pw=min(pw+0.5,25)
    elif pw>0: b[0][2],b[0][3],pw,t=pw*m.cos(a)*0.8,pw*m.sin(a)*0.8,0,2
    if pw>=0:
     pg.draw.line(s,(255,255,255),(b[0][0],b[0][1]),(b[0][0]+m.cos(a)*80,b[0][1]+m.sin(a)*80),1)
     ox,oy=b[0][0]-m.cos(a)*(15+pw),b[0][1]-m.sin(a)*(15+pw)
     pg.draw.line(s,(139,69,19),(ox,oy),(ox-m.cos(a)*(50+pw),oy-m.sin(a)*(50+pw)),6)
   elif t==2:
    ta=[l for l in b if l[5]==2]; tg=r.choice(ta) if ta else b[0]; a=m.atan2(tg[1]-b[0][1],tg[0]-b[0][0])+(r.random()-0.5)*(1-sk)
    b[0][2],b[0][3],t=12*m.cos(a),12*m.sin(a),1
  for pk in [(28,28),(400,20),(772,28),(28,372),(400,380),(772,372)]: pg.draw.circle(s,(0,0,0),pk,28)
  for i,l in enumerate(b):
   l[0]+=l[2]; l[1]+=l[3]; l[2]*=0.985; l[3]*=0.985
   if l[0]<30 or l[0]>770: l[2]*=-1; l[0]=30 if l[0]<30 else 770
   if l[1]<30 or l[1]>370: l[3]*=-1; l[1]=30 if l[1]<30 else 370
   for j,o in enumerate(b):
    if i<j:
     dx,dy=o[0]-l[0],o[1]-l[1]; dst=m.hypot(dx,dy)
     if dst<20:
      ang=m.atan2(dy,dx); s_a,c_a=m.sin(ang),m.cos(ang); v1,v2=l[2]*c_a+l[3]*s_a,o[2]*c_a+o[3]*s_a
      l[2],l[3],o[2],o[3]=l[2]+(v2-v1)*c_a,l[3]+(v2-v1)*s_a,o[2]+(v1-v2)*c_a,o[3]+(v1-v2)*s_a
      mt=(20.1-dst)/2; l[0]-=c_a*mt; l[1]-=s_a*mt; o[0]+=c_a*mt; o[1]+=s_a*mt
   for pk in [(28,28),(400,20),(772,28),(28,372),(400,380),(772,372)]:
    if m.hypot(l[0]-pk[0],l[1]-pk[1])<28:
     if l[4]==8: gm,wn=1,("AI" if t==1 else "Player")
     elif i==0: l[0],l[1],l[2],l[3]=200.0,200.0,0.0,0.0
     else: b.pop(i)
   pg.draw.circle(s,(0,0,0),(int(l[0]),int(l[1])),11); pg.draw.circle(s,l[6],(int(l[0]),int(l[1])),10)
   if l[5]==2: pg.draw.line(s,(255,255,255),(l[0]-8,l[1]),(l[0]+8,l[1]),2)
   if l[4]>0: s.blit(f.render(str(l[4]),1,(255,255,255) if l[4]==8 else (0,0,0)),(l[0]-5,l[1]-7))
 else:
  txt=f.render(f"{wn} Wins! Play again? (Y/N)",1,(255,255,255)); s.blit(txt,(400-txt.get_width()//2,180))
 pg.display.flip(); c.tick(60)
pg.quit()