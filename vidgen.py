# -*- coding: utf-8 -*-
from __future__ import division
import mlt
import time, os, math
import sys, json
import pathlib
import tempfile
import urllib
import urllib2
from PIL import Image
import langid
from utils import *
import re
def textembedder(cc, cs, cf, ca, credit, deffontsize, scene, lindex, title_screen, question_text, intro_screen, outro_screen):
	if cc:
		scp= cc.split(",")		
		pleft, init_top= scp[0],int(scp[1])
	else:
		pleft, init_top = 0, 0
    	if cs:
		pxsize = cs
    	else:
		pxsize = deffontsize
        font = get_font(cf)			
	lines=process_text(credit)
	height=0
	align = ca
	rightpoint = 0 
	centerpoint = 0
	maxwidth = 0
	widths= []
        for line in lines:
		if line.strip()!="" and line.strip()!="&nbsp;":		
			tline='<span font="'+str(pxsize)+'" face="'+font+'">'+ line  +'</span>'
			#print str(pleft)+ "  "+ tline+ "  "+ str(init_top)
			tf=tempfile.NamedTemporaryFile(mode='w+b',  suffix='.png', prefix='tmp_'+str(int(time.time())), delete=False, dir=outdir)
			ftodel.append(tf.name)
			tf2=tempfile.NamedTemporaryFile(mode='w+b',  suffix='.txt', prefix='tmp_'+str(int(time.time())), delete=False, dir=outdir)
			ftodel.append(tf2.name)
			write_png2(tline, tf.name, tf2.name )
			try:		
			    	img = Image.open(tf.name)
			    	width, height = img.size
			except:
				width, height = 0, 0
 			widths.append(width)
	maxwidth = max(widths)
	rightpoint = int(pleft) + int(maxwidth)
	centerpoint = int(pleft) +int(maxwidth/2)
        for line in lines:
		if line.strip()!="" and line.strip()!="&nbsp;":		
			tline='<span font="'+str(pxsize)+'" face="'+font+'">'+ line  +'</span>'
			#print str(pleft)+ "  "+ tline+ "  "+ str(init_top)
			tf=tempfile.NamedTemporaryFile(mode='w+b',  suffix='.png', prefix='tmp_'+str(int(time.time())), delete=False, dir=outdir)
			ftodel.append(tf.name)
			tf2=tempfile.NamedTemporaryFile(mode='w+b',  suffix='.txt', prefix='tmp_'+str(int(time.time())), delete=False, dir=outdir)
			ftodel.append(tf2.name)
			write_png2(tline, tf.name, tf2.name )
			try:		
			    	img = Image.open(tf.name)
			    	width, height = img.size
			except:
				width, height = 0, 0 
			f = mlt.Filter(profile, "watermark:"+tf.name)
			if title_screen:
				if align == 'left' or lindex == 0:	
				    	f.set("composite.geometry",str(pleft)+"/"+str(init_top)+":0%x0%;10="+str(pleft)+"/"+str(init_top)+":100%x100%;")
				elif align == 'right':
						npleft = rightpoint - width
						f.set("composite.geometry",str(npleft)+"/"+str(init_top)+":0%x0%;10="+str(npleft)+"/"+str(init_top)+":100%x100%;")
				elif align == 'center':
						npleft = centerpoint - int(width/2)
						f.set("composite.geometry",str(npleft)+"/"+str(init_top)+":0%x0%;10="+str(npleft)+"/"+str(init_top)+":100%x100%;")
				f.set('in',((lindex)*20))
					
			elif outro_screen:
				if align == 'left' or lindex == 0:	
			    		f.set('composite.start',str(pleft)+'/'+str(init_top)+':100%x100%')
				elif align == 'right':
					npleft = rightpoint - width
					f.set('composite.start',str(npleft)+'/'+str(init_top)+':100%x100%')
				elif align == 'center':
					npleft = centerpoint - int(width/2)
					f.set('composite.start',str(npleft)+'/'+str(init_top)+':100%x100%')
				f.set('in',0)
			elif question_text:
				if align == 'left' or (rightpoint == 0 and centerpoint==0):	
			    		f.set('composite.start',str(pleft)+'/'+str(init_top)+':100%x100%')
				elif align == 'right':
					npleft = rightpoint - width
					f.set('composite.start',str(npleft)+'/'+str(init_top)+':100%x100%')
				elif align == 'center':
					npleft = centerpoint - int(width/2)
					f.set('composite.start',str(npleft)+'/'+str(init_top)+':100%x100%')
		   		f.set('in',40)
			elif intro_screen:
				if init_top == 0:
					if profile.width() <1080:
						init_top = int((profile.height()*30)/100)

					else:
						init_top = int((profile.height()*20)/100)
					pleft = int((profile.width()-width)/2)
				f.set('composite.start',str(pleft)+'/'+str(init_top)+':100%x100%')
				f.set('in',10)
				f.set('out',28)		
			else:						      
				if rightpoint == 0 and centerpoint==0:			
					f.set("composite.geometry","-1500/"+str(init_top)+":0%x0%;20="+str(pleft)+"/"+str(init_top)+":100%x100%;")
			    		f.set('in',((lindex+2)*20))
				else:
					if align == 'left':
						f.set("composite.geometry","-1500/"+str(init_top)+":0%x0%;20="+str(pleft)+"/"+str(init_top)+":100%x100%;")
					elif align == 'right':
						npleft = rightpoint - width
						f.set("composite.geometry","-1500/"+str(init_top)+":0%x0%;20="+str(npleft)+"/"+str(init_top)+":100%x100%;")
					elif align == 'center':
						npleft = centerpoint - int(width/2)
						f.set("composite.geometry","-1500/"+str(init_top)+":0%x0%;20="+str(npleft)+"/"+str(init_top)+":100%x100%;")
			   		f.set('in',(3*20)+5*lindex)			
			init_top+=height+5		
			scene.attach(f)
			lindex+=1
		else:
		
			try:
				init_top+=height+5
			except:
				try:
					init_top+=50+5
				except:
					pass
	return lindex		    	




def create_overlay_screen():
	global profile
	scene = mlt.Producer(profile, "colour:#E53B07")
	f = mlt.Filter(profile, "affine")
	f.set('transition.distort',1)
	f.set('transitioLD_PRELOAD=n.fill',1)
	f.set('transition.scale_y',1)
	if profile.width() == 1920:
		f.set('transition.fix_rotate_x',0)
		f.set('transition.fix_shear_y',45)
		f.set('transition.geometry',"0=-50%/0%:120%x100%;5=-10%/0:120%x100%;25=-10%/0:120%x100%;30=150%/0%:120%x100%;")
	else:
		f.set('transition.fix_rotate_x',40)
		f.set('transition.fix_shear_y',60)
		f.set('transition.geometry',"0=-0/-150%:160%x200%;5=0/-70%:160%x200%;25=0/-70%:160%x200%;35=50%/150%:150%x200%;")
	scene.attach(f)
	scene.set('out',30)
	return scene


def create_scene(media):
	if media.endswith(".gif"):
		tv=tempfile.NamedTemporaryFile(mode='w+b',  suffix='.mp4', prefix='tmp', delete=False, dir=outdir)
		subprocess.call(["ffmpeg", "-i", media, "-y",  tv.name,"-loglevel", "quiet"])
		ftodel.append(tv.name)
		tscene = mlt.Producer(profile, tv.name)
		if tscene.get_out() == 0:
			tp=tempfile.NamedTemporaryFile(mode='w+b',  suffix='.gif', prefix='tmp', delete=False, dir=outdir)
			ftodel.append(tp.name)
			subprocess.call(["ffmpeg", "-i", media, "-y","-loglevel", "quiet",  tp.name])
			scene = mlt.Producer(profile, tp.name)
		elif tscene.get_out() < 150:
			scene=mlt.Playlist()
			lt = int(150/tscene.get_out())+1
			for x in range(0, lt):
				tscene = mlt.Producer(profile, tv.name)
				scene.append(tscene)
			scene.set('out', 150)
		else:
			scene = mlt.Producer(profile, tv.name)
	elif media.endswith(".mp3"):
		tv=tempfile.NamedTemporaryFile(mode='w+b',  suffix='.wav', prefix='tmp', delete=False, dir=outdir)
		subprocess.call(["ffmpeg", "-i", media, "-y",  tv.name,"-loglevel", "quiet"])
		ftodel.append(tv.name)
		scene = mlt.Producer(profile, tv.name)
	
	elif media.startswith("http"):
		extension = media[media.rfind("."):]
		tv=tempfile.NamedTemporaryFile(mode='w+b',  suffix=extension, prefix='tmp', delete=False, dir=outdir)
		ftodel.append(tv.name)
		subprocess.call(["ffmpeg", "-i", media, "-y","-c:a", "copy", "-c:v", "copy","-loglevel", "quiet",  tv.name])
		#subprocess.call(["ffmpeg", "-i", media, "-y",  tv.name])
		scene = mlt.Producer(profile, tv.name)
	else:
		scene = mlt.Producer(profile, media)
	return scene
oscene_index = 0	
def process_scene(sc, ss, sf, sa, s, cc, cs, cf, ca, credit, qc, qs, qf, qa, question, title_screen, scene):
    global outdir, scenes, oscenes, oscene_index, current_scene, t_scenes, ftodel, profile, dark_filter
    	
    sl = scene.get_out()	
    if title_screen:
	oscenes.insert_blank(oscene_index, (sl-10))
	oscene_index+=1

    if sl==150:			
	    f = mlt.Filter(profile, "crop")
	    f.set('center',1)
	    scene.attach(f)
	    f = mlt.Filter(profile, "affine")
	    f.set('background','colour:1')
	    if title_screen:		
		    f.set('transition.geometry',"0=-10%/-20%:120%x120%;10=-10%/0:120%x120%;20=-10%/0:120%x120%;140=0/0:100%x100%;150=0/0:120%x120%;")
	    else:
		    f.set('transition.geometry',"0=-150%/-150%:350%x350%;30=0/0:100%x100%;40=0/0:100%x100%;150=-5%/-5%:110%x110%;")
		    b = mlt.Filter(profile, "boxblur")
	    	    b.set('in',0)
		    b.set('out',20)
	    	    b.set('blur',200)
	    	    scene.attach(b)
	    scene.attach(f)
	    if (title_screen or (current_scene < t_scenes)) :	
	    	b = mlt.Filter(profile, "boxblur")
	    	b.set('in',(sl-5))
	    	b.set('start',200)
	    	b.set('end',400)
	    	scene.attach(f)
	    	scene.attach(b)

    	
    init_top=400
    last_top=400
    lindex = 0 			
    if question is not None and question!="":
	lx=textembedder(qc, qs, qf, qa, question, 50, scene, 0, title_screen, 1, 0 , 0)

	oscene=create_overlay_screen()
	lx=textembedder("0,0", qs, qf, qa, question, 50, oscene, 0, 0, 0, 1, 0)
	oscenes.append(oscene)
	oscene_index+=1
	oscenes.insert_blank(oscene_index, (sl-30))
	oscene_index+=1
    if s is not None and s!="":
    	lindex=textembedder(sc, ss, sf, sa, s, 25, scene, 0, title_screen, 0, 0, 0)	   	
    if credit is not None and credit!="":
	l=textembedder(cc, cs, cf, ca, credit, 20, scene, lindex, 0, 0, 0, 0)

config = json.loads(file_content(sys.argv[1]))
s=str(sys.argv[1])
uid = sys.argv[2]
vid = sys.argv[3]

ftodel=list()
t_scenes=scene_count(config)
current_scene=0
pjson = {'Progress': 'True', 'video': ''}

fgcolor=config["23"][9]['font_color__23']
bgcolor=config["23"][4]['highlight_color__23']
vtype=config["0"][0]['format']

mlt.mlt_log_set_level(0) # verbose
mlt.Factory().init( )

logo_max_size=0
if vtype == 'square':	
	profile = mlt.Profile()
	profile.set_explicit(1)
	profile.set_sample_aspect(1, 1)
	profile.set_frame_rate(30000, 1000)
	profile.set_display_aspect(1, 1)
	profile.set_width(1080)	
	profile.set_height(1080)
	profile.set_colorspace(709)
	logo_max_size = 125
elif vtype == 'vertical':
	profile = mlt.Profile()
	profile.set_explicit(1)
	profile.set_sample_aspect(1, 1)
	profile.set_frame_rate(30000, 1000)
	profile.set_display_aspect(2, 3)
	profile.set_width(720)
	profile.set_height(1080)
	profile.set_colorspace(709)
	logo_max_size = 100
else:	
	profile = mlt.Profile("atsc_1080p_30")
	logo_max_size = 160	
	
profile.set_colorspace(709)

tractor = mlt.Tractor()
scenes=mlt.Playlist()
oscenes=mlt.Playlist()
sindex = 1
slength = 5
t_length = 0
frame_rate = 30
production = 0		
if production:
	save_video = 1
	outdir=s[0:s.rfind("/")]
else:
	save_video = 0
	outdir=s[0:s.rfind("/")]+"/Temp"
#outdir="/home/prftp/html/docroot/backend/web/python"

outroshow=int(config["27"][4]["display_outro__27"])
outrocol=config["27"][9]["background_color_outro__27"]
outrologo=config["27"][14]["logo_outro__27"]
outrovideo=config["27"][19]["video_outro__27"]

logo=config["24"][4]["main_logo__24"]
dark_filter=config["25"][4]["dark_filter_footages__25"]


music=config["26"][4]["music_file__26"]
music_or_footage=config["26"][9]["music_type__26"]
footage_vol=int(config["26"][19]["audio_level__26"])
music_vol=int(config["26"][14]["music_level__26"])


if music_or_footage=='music_only':
	scenes.set('hide',2)
gain_filter = mlt.Filter(profile, "avfilter.volume")
gain_filter.set("av.volume", str(footage_vol/100))
scenes.attach(gain_filter)


media=config["1"][9]["media__1"]
media=media.strip()
title=config["1"][4]["title__1"]
scene=create_scene(str(media))
if scene.get_out()==14999:
	scene.set('out',150)


t_length+=scene.get_out()
process_scene(config["1"][0]["coordinate_title__1"],config["1"][1]["font_size_title__1"],config["1"][2]["font_family_title__1"],config["1"][3]["text_alignment_title__1"],title,config["1"][10]["coordinate_credit__1"],config["1"][11]["font_size_credit__1"], config["1"][12]["font_family_credit__1"], config["1"][13]["text_alignment_credit__1"], config["1"][14]["credit__1"],None,None,None,None,None,1,scene)



scenes.append(scene)
for x in range(2, 22):
	if config[str(x)][9]["answer__"+str(x)]:
	
		#print "media: "+ config[str(x)][1]["answer__"+str(x)]
		media=config[str(x)][9]["answer__"+str(x)]
		media=media.strip()
		scene=create_scene(str(media))

		sindex+=1
		if scene.get_out()==14999: scene.set('out',150)
		t_length+=scene.get_out()

		current_scene+=1
		#if config[str(x)][11]["subtitles__"+str(x)]:
		process_scene(config[str(x)][10]["coordinate_subtitles__"+str(x)],config[str(x)][11]["font_size_subtitles__"+str(x)],config[str(x)][12]["font_family_subtitles__"+str(x)],config[str(x)][13]["text_alignment_subtitles__"+str(x)], config[str(x)][14]["subtitles__"+str(x)], config[str(x)][15]["coordinate_credit__"+str(x)], config[str(x)][16]["font_size_credit__"+str(x)] , config[str(x)][17]["font_family_credit__"+str(x)] , config[str(x)][18]["text_alignment_credit__"+str(x)], config[str(x)][19]["credit__"+str(x)], config[str(x)][0]["coordinate_question__"+str(x)], config[str(x)][1]["font_size_question__"+str(x)], config[str(x)][2]["font_family_question__"+str(x)], config[str(x)][3]["text_alignment_question__"+str(x)], config[str(x)][4]["question__"+str(x)], 0,scene)
		#print media

		scenes.append(scene)

if logo:
	extension = str(logo)[str(logo).rfind("."):]
	tv=tempfile.NamedTemporaryFile(mode='w+b',  suffix=extension, prefix='tmp', delete=False, dir=outdir)
	subprocess.call(["ffmpeg", "-i", str(logo), "-y",  tv.name,"-loglevel", "quiet"])
	f = mlt.Filter(profile, "watermark:"+str(tv.name))
	ftodel.append(tv.name)	
    	im = Image.open(str(tv.name))
    	width, height = im.size
	if width > logo_max_size:
		asp= width/height
		width = logo_max_size
		height = int(asp*width)
	logoc=config["24"][0]["coordinate_main_logo__24"]
	if logoc:
		scp= logoc.split(",")		
		logoleft, logotop= scp[0],int(scp[1])
	else:
		logoleft, logotop = 0, 0
#	print " Logo height: "+str(height)+"   Logog width: "+ str(width)
#	f.set('composite.start','80%/5%:100%x100%')
#	f.set('composite.start',str(profile.width()-width-25)+'/25:'+str(width)+'x'+str(height))
	f.set('composite.start',str(logoleft)+'/'+str(logotop)+':100%x100%')
	scenes.attach(f)
	f.set('out',t_length)

scene=""
if outroshow!=2:

	if outrologo:
		scene=create_scene (str(outrologo))
	elif outrovideo:
		scene=create_scene(str(outrovideo))
		#f = mlt.Filter(profile, "watermark:"+str(outrovideo))
		#f.set('composite.halign','center')
		#f.set('composite.valign','middle')
		#f.set('prducer.loop', 0)
		#ts=create_scene(str(outrovideo))		
		if scene.get_out()==14999: scene.set('out',150)
		else : scene.set('out',scene.get_out())
		#scene.attach(f)
	elif outrocol:
		scene=mlt.Producer(profile, 'colour:'+str(outrocol))

	if config["27"][24]["text_outro__27"] and scene:
		line=process_text(config["27"][24]["text_outro__27"])
		l=textembedder(config["27"][20]["coordinate_text_outro__27"], config["27"][21]["font_size_text_outro__27"], config["27"][22]["font_family_text_outro__27"], config["27"][23]["text_alignment_text_outro__27"], config["27"][24]["text_outro__27"], 40, scene, 0, 0, 0, 0, 1)

	if config["27"][29]["credits_outro__27"] and scene:
		l=textembedder(config["27"][25]["coordinate_credits_outro__27"], config["26"][21]["font_size_credits_outro__27"], config["27"][27]["font_family_credits_outro__27"], config["27"][28]["text_alignment_credits_outro__27"], config["27"][29]["credits_outro__27"], 40, scene, 0, 0, 0, 0, 1)
	if scene:
		if scene.get_out()==14999: scene.set('out',150)
		t_length+=scene.get_out()
		scenes.append(scene)


tractor.multitrack().connect(scenes,0)
tractor.multitrack().connect(oscenes,1)
transition = mlt.Transition(profile, "composite")
transition.set("a_track", 0)
transition.set("b_track", 1)
transition.set("sliced_composite", 1)
tractor.plant_transition(transition, 0, 1)

if music and music_or_footage!='footage_only':
	tsound = mlt.Producer(profile, str(music))
	if tsound.get_out() < t_length:
		sound=mlt.Playlist()
		lt= int(t_length/tsound.get_out())+1
		for x in range(0, lt):
			tsound = mlt.Producer(profile, str(music))
			sound.append(tsound)
	else:
		sound = mlt.Producer(profile, str(music))
	sound.set('out',t_length)
	#print str(t_length)
	gain_filter = mlt.Filter(profile, "avfilter.volume")
	gain_filter.set("av.volume", str(music_vol/100))
	sound.attach(gain_filter)

	tractor.multitrack().connect(sound, 2)
	transition = mlt.Transition(profile, "mix")
	transition.set("a_track", 0)
	transition.set("b_track", 2)
	transition.set("always_active", 1)
	transition.set("sum", 1)
	tractor.plant_transition(transition, 0, 2)


if save_video:
	c = mlt.Consumer(profile, "avformat")
	tv=tempfile.NamedTemporaryFile(mode='w+b',  suffix='.mp4', prefix='tmp', delete=False, dir=outdir)
	c.set('target',str(tv.name))
else:
	c = mlt.Consumer(profile, "sdl")
	
c.set('resize','none')
c.set('strict', '-2')



c.connect_producer(tractor)
c.set("terminate_on_pause", 1)
c.start()

while c.is_stopped() == 0:
	time.sleep(1)
	percent=str(int(math.floor((scenes.frame()*100)/scenes.get_length())))
	if production:
		pjson['Progress']=percent
		values = {'user_id' : uid,
          	'video_id' : vid,
	  	'token' : 'ZK2xcDVghfgSGnseg1fYdY7',
          	'json' : pjson }
		url="https://urp"
		output=urllib2.urlopen('url?token=ZK2xcDVghfgSGnseg1fYdY7&video_id='+vid+'&user_id='+uid+'&json={%22Progress%22%3A+%22'+str(percent)+'%22%2C+%22video%22%3A+%22%22}').read()
		print output
	else:
		print percent
if save_video:
	os.chmod(tv.name, 0644)
	print "video file:  "+ tv.name
	pjson['video']=tv.name
	output=urllib2.urlopen('url?token=ZK2xcDVghfgSGnseg1fYdY7&video_id='+vid+'&user_id='+uid+'&json={%22Progress%22%3A+%22'+str(percent)+'%22%2C+%22video%22:%20%22'+tv.name+'%22%20}').read()
	print output
#for f in ftodel:
#	os.remove(f) 
