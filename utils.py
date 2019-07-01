# -*- coding: utf-8 -*-
import sys
import codecs
import json
import cairocffi
import cffi
import subprocess
from PIL import Image
ffi = cffi.FFI()
import os
ffi.cdef('''
    /* GLib */
    typedef void cairo_t;
    typedef void* gpointer;
    void g_object_unref (gpointer object);

    /* Pango and PangoCairo */
    typedef ... PangoLayout;
    typedef enum {
        PANGO_ALIGN_LEFT,
        PANGO_ALIGN_CENTER,
        PANGO_ALIGN_RIGHT
    } PangoAlignment;
    int pango_units_from_double (double d);
    PangoLayout * pango_cairo_create_layout (cairo_t *cr);
    void pango_cairo_show_layout (cairo_t *cr, PangoLayout *layout);
    void pango_layout_set_width (PangoLayout *layout, int width);
    void pango_layout_set_alignment (
        PangoLayout *layout, PangoAlignment alignment);
    void pango_layout_set_markup (
        PangoLayout *layout, const char *text, int length);
''')
gobject = ffi.dlopen('gobject-2.0')
pango = ffi.dlopen('pango-1.0')
pangocairo = ffi.dlopen('pangocairo-1.0')

gobject_ref = lambda pointer: ffi.gc(pointer, gobject.g_object_unref)
units_from_double = pango.pango_units_from_double
def write_png(width, target,markup):
    if width < 1080: width-=100	
    else: width-=200
    pt_per_mm = 72 / 25.4
    height = 1080
    surface = cairocffi.PDFSurface(target, width, height)
    surface = cairocffi.ImageSurface(cairocffi.FORMAT_ARGB32, width, height)
    surface. set_mime_data("image/png", None)	
    context = cairocffi.Context(surface)
    context.translate(0, 300)
    #context.rotate(-0.2)

    layout = gobject_ref(
        pangocairo.pango_cairo_create_layout(context._pointer))
    pango.pango_layout_set_width(layout, units_from_double(width))
    pango.pango_layout_set_alignment(layout, pango.PANGO_ALIGN_LEFT)
    markup = ffi.new('char[]', markup.encode('utf8'))
    pango.pango_layout_set_markup(layout, markup, -1)
    pangocairo.pango_cairo_show_layout(context._pointer, layout)
    surface.write_to_png(target)	
def write_png_center(width, target,markup):
    pt_per_mm = 72 / 25.4
    height = 1080
    surface = cairocffi.PDFSurface(target, width, height)
 	
    surface = cairocffi.ImageSurface(cairocffi.FORMAT_ARGB32, width, height)
    surface. set_mime_data("image/png", None)	
    context = cairocffi.Context(surface)
    context.translate(0, 300)
    #context.rotate(-0.2)

    layout = gobject_ref(
        pangocairo.pango_cairo_create_layout(context._pointer))
    pango.pango_layout_set_width(layout, units_from_double(width))
    pango.pango_layout_set_alignment(layout, pango.PANGO_ALIGN_CENTER)
    markup = ffi.new('char[]', markup.encode('utf8'))
    pango.pango_layout_set_markup(layout, markup, -1)
    pangocairo.pango_cairo_show_layout(context._pointer, layout)
    surface.write_to_png(target)
def savejson(filename,data):
    with open(filename, 'w') as outfile:
	res = json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))
def file_content(file):
    f = open(file, 'r')
    fc = f.read()
    fc = fc.strip()
    f.close()
    return fc
def scene_count(config):
    count=0
    for x in range(2, 22):
	if config[str(x)][9]["answer__"+str(x)]:
		count+=1
    return count
def get_font(sf):
    if sf:
	if sf == "comic-sans":
		font = "Comic Sans MS, Arial"
	elif sf == "roboto":
		font = "Roboto, Scheherazade"
	elif sf == "lato":
		font = "Lato, Scheherazade"
	elif sf == "georgia":
		font = "Georgia, Scheherazade"
	elif sf == "tahoma":
		font = "Tahoma"
	elif sf == "verdana":
		font = "Verdana, Scheherazade"
	elif sf == "georgia":
		font = "Georgia, Scheherazade"
	elif sf == "arial":
		font = "Arial, Scheherazade"
	elif (sf == "bodonifont" or sf == "bodoni"):
		font = "bodoni, Arial"
	elif (sf == "garamond" or sf == "Garamond"):
		font = "Garamond, Scheherazade"
    else:
	font = "Roboto, Scheherazade" 

   	
    return font 
def write_png2(text, file , infile):
	text=text.replace("&nbsp;"," ")	
	t=u''
	t = t + text
	text = t
	f = codecs.open(infile, "w", "utf-8")
	f.write(text)
	f.close() 
	subprocess.call(["pango-view","--background", "transparent", "--markup", infile, "--pixels","--margin=0px", "-q", "-o",   file])
	#subprocess.call("pango-view --markup  "+ infile +" --pixels --margin=0px  -q -o "+  file +" --background=transparent", shell=False)
	#print "pango-view --markup -t '"+ text +"' --pixels --margin=0px  -q -o "+  file +" --background=transparent"
	#os.system("pango-view --markup -t '"+ text +"' --pixels --margin=0px  -q -o "+  file +" --background=transparent")
	#p = subprocess.Popen(["pango-view", "--markup", "-t", text, "--pixels","--margin=0px", "-q", "-o",   file, "--background=transparent"], stdout=subprocess.PIPE, 
        #   stderr=subprocess.STDOUT)
	#print p.communicate()

def process_text(text):
	flines=[]
	text=text.replace("<br />","</p><p>")	
	lines= text.split('</p>')
	for line in lines:
		line = line.replace("<p>","")
		line = line.replace("</em>","</i>").replace("<em>","<i>")
		line = line.replace("</strong>","</b>").replace("<strong>","<b>")
		line = line.replace('style=\"color:','foreground="').replace('\">','">')
		line = line.replace('style=\"background-color:','background="').replace('\">','">')
		flines.append(line)
	return flines	

def process_text_vfx(text):
	flines=[]
	text=text.replace("<br />","</p><p>")	
	lines= text.split('</p>')
	for line in lines:
		line = line.replace("<p>","")
		#line = line.replace("</em>","</i>").replace("<em>","<i>")
		#line = line.replace("</strong>","</b>").replace("<strong>","<b>")
		#line = line.replace('style=\"color:','foreground="').replace('\">','">')
		#line = line.replace('style=\"background-color:','background="').replace('\">','">')
		flines.append(line)
	return flines

html="""
<html>
<head>
<meta charset="UTF-8">
<style type="text/css">
*{padding: 0;margin: 0;}
html, body {height: 100%;}
"""
html1="""

.slide-left {
  width:100%;
  overflow:hidden;
   -webkit-animation: slide-left 1s;

}

@-webkit-keyframes slide-left {
  from {
    margin-left: 50%;
    width: 200%;
    opacity: 0; 
  }

  to {
    margin-left: 0%;
    width: 100%;
    opacity: 1;	
  }
}


.slide-right {
  width:100%;
  overflow:hidden;
   -webkit-animation: slide-right 1s;
}


@-webkit-keyframes slide-right {
  from {
    margin-left: -20%;
    width: 100%;
    opacity: 0; 
  }

  to {
    margin-left: 0%;
    width: 100%;
    opacity: 1;	
  }
}
#grad1 {
  height: 800px;
background: -webkit-linear-gradient(top,rgba(0, 0, 0, 0) 0%,rgba(0, 0, 0, 0.1) 20%,rgba(0, 0, 0, 0.3) 40%,rgba(0, 0, 0, 0.5) 60%,rgba(0, 0, 0, 0.7) 80%,rgba(0, 0, 0, 1) 100%); /* Chrome10-25,Safari5.1-6 */
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  padding: 1rem;

  text-align: center;
  z-index: 1;
}

</style>

<script type="text/javascript">
function onLoad() {
    webvfx.readyRender(true);
}
window.addEventListener("load", onLoad, false);
</script>
</head>
<body>
<div id="text">
"""	
html2="""
.slide-left {
  width:100%;
  overflow:hidden;
   -webkit-animation: slide-left 2s;
   -webkit-animation-direction: forwards;
   -webkit-animation-fill-mode: forwards;
}



@-webkit-keyframes slide-left {
  from {
    margin-left: 0%;
    width: 100%;
    opacity: 1;	
  }

  to {
    margin-left: 50%;
    width: 200%;
    opacity: 0; 

  }
}


.slide-right {
  width:100%;
  overflow:hidden;
   -webkit-animation: slide-right 2s;
   -webkit-animation-direction: forwards;
   -webkit-animation-fill-mode: forwards;

}


@-webkit-keyframes slide-right {
  from {
    margin-left: 0%;
    width: 100%;
    opacity: 1;	

  }
  to {
    margin-left: -20%;
    width: 100%;
    opacity: 0; 
  }
}


#grad1 {
  height: 800px;
background: -webkit-linear-gradient(top,rgba(0, 0, 0, 0) 0%,rgba(0, 0, 0, 0.1) 20%,rgba(0, 0, 0, 0.3) 40%,rgba(0, 0, 0, 0.5) 60%,rgba(0, 0, 0, 0.7) 80%,rgba(0, 0, 0, 1) 100%); /* Chrome10-25,Safari5.1-6 */
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  padding: 1rem;

  text-align: center;
  z-index: 1;
}

</style>

<script type="text/javascript">
function onLoad() {
    webvfx.readyRender(true);
}
window.addEventListener("load", onLoad, false);
</script>
</head>
<body>
<div id="text">
"""	
