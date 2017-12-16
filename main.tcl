#############################################################################
# Generated by PAGE version 4.9
# in conjunction with Tcl version 8.6
set vTcl(timestamp) ""


set vTcl(actual_gui_bg) #d9d9d9
set vTcl(actual_gui_fg) #000000
set vTcl(actual_gui_menu_bg) #d9d9d9
set vTcl(actual_gui_menu_fg) #000000
set vTcl(complement_color) #d9d9d9
set vTcl(analog_color_p) #d9d9d9
set vTcl(analog_color_m) #d9d9d9
set vTcl(active_fg) #000000
set vTcl(actual_gui_menu_active_bg)  #d8d8d8
set vTcl(active_menu_fg) #000000
#############################################################################
# vTcl Code to Load User Fonts

vTcl:font:add_font \
    "-family Georgia -size 9 -weight normal -slant roman -underline 0 -overstrike 0" \
    user \
    vTcl:font10
vTcl:font:add_font \
    "-family Georgia -size 12 -weight normal -slant roman -underline 0 -overstrike 0" \
    user \
    vTcl:font9
#################################
#LIBRARY PROCEDURES
#


if {[info exists vTcl(sourcing)]} {

proc vTcl:project:info {} {
    set base .top37
    namespace eval ::widgets::$base {
        set dflt,origin 0
        set runvisible 1
    }
    namespace eval ::widgets_bindings {
        set tagslist _TopLevel
    }
    namespace eval ::vTcl::modules::main {
        set procs {
        }
        set compounds {
        }
        set projectType single
    }
}
}

#################################
# USER DEFINED PROCEDURES
#

#################################
# GENERATED GUI PROCEDURES
#

proc vTclWindow.top37 {base} {
    if {$base == ""} {
        set base .top37
    }
    if {[winfo exists $base]} {
        wm deiconify $base; return
    }
    set top $base
    ###################
    # CREATING WIDGETS
    ###################
    vTcl::widgets::core::toplevel::createCmd $top -class Toplevel \
        -background {#d9d9d9} -highlightbackground {#d9d9d9} \
        -highlightcolor black 
    wm focusmodel $top passive
    wm geometry $top 901x450+511+97
    update
    # set in toplevel.wgt.
    global vTcl
    set vTcl(save,dflt,origin) 0
    wm maxsize $top 1924 1057
    wm minsize $top 140 1
    wm overrideredirect $top 0
    wm resizable $top 1 1
    wm deiconify $top
    wm title $top "Chinese"
    vTcl:DefineAlias "$top" "mainscreen" vTcl:Toplevel:WidgetProc "" 1
    listbox $top.lis38 \
        -background white -disabledforeground {#a3a3a3} -font TkFixedFont \
        -foreground {#000000} -height 328 -highlightbackground {#d9d9d9} \
        -highlightcolor black -selectbackground {#c4c4c4} \
        -selectforeground black -width 294 
    .top37.lis38 configure -font TkFixedFont
    .top37.lis38 insert end text
    vTcl:DefineAlias "$top.lis38" "unitList" vTcl:WidgetProc "mainscreen" 1
    label $top.lab39 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Select Unit} 
    vTcl:DefineAlias "$top.lab39" "unitSelect" vTcl:WidgetProc "mainscreen" 1
    button $top.but40 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -borderwidth 3 -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -pady 0 \
        -text {Add New Unit} 
    vTcl:DefineAlias "$top.but40" "newUnit" vTcl:WidgetProc "mainscreen" 1
    label $top.lab41 \
        -activebackground {#000080} -activeforeground {#000000} \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Select a unit to start} 
    vTcl:DefineAlias "$top.lab41" "vocabWordLabel" vTcl:WidgetProc "mainscreen" 1
    button $top.cpd38 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -borderwidth 3 -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font10,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -padx 0 -pady 0 \
        -text {Pinyin Mode!} 
    vTcl:DefineAlias "$top.cpd38" "pinyinModeButton" vTcl:WidgetProc "mainscreen" 1
    button $top.cpd39 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -borderwidth 3 -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font10,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -padx 0 -pady 0 \
        -text {Definition Mode!} 
    vTcl:DefineAlias "$top.cpd39" "defModeButton" vTcl:WidgetProc "mainscreen" 1
    button $top.cpd37 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -borderwidth 3 -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font10,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -padx 0 -pady 0 \
        -text {Character Mode!} 
    vTcl:DefineAlias "$top.cpd37" "charModeButton" vTcl:WidgetProc "mainscreen" 1
    checkbutton $top.che40 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font10,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -justify left \
        -text {Hard Mode} -variable hardMode 
    vTcl:DefineAlias "$top.che40" "toggleHardButton" vTcl:WidgetProc "mainscreen" 1
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.lis38 \
        -in $top -x 10 -y 50 -width 294 -relwidth 0 -height 328 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.lab39 \
        -in $top -x 100 -y 10 -width 102 -relwidth 0 -height 26 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but40 \
        -in $top -x 10 -y 390 -width 296 -relwidth 0 -height 43 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.lab41 \
        -in $top -x 410 -y 150 -width 352 -relwidth 0 -height 116 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $top.cpd38 \
        -in $top -x 530 -y 390 -width 155 -height 43 -anchor nw \
        -bordermode inside 
    place $top.cpd39 \
        -in $top -x 710 -y 390 -width 175 -relwidth 0 -height 43 -relheight 0 \
        -anchor nw -bordermode inside 
    place $top.cpd37 \
        -in $top -x 350 -y 390 -width 155 -height 43 -anchor nw \
        -bordermode inside 
    place $top.che40 \
        -in $top -x 790 -y 10 -anchor nw -bordermode ignore 

    vTcl:FireEvent $base <<Ready>>
}

#############################################################################
## Binding tag:  _TopLevel

bind "_TopLevel" <<Create>> {
    if {![info exists _topcount]} {set _topcount 0}; incr _topcount
}
bind "_TopLevel" <<DeleteWindow>> {
    if {[set ::%W::_modal]} {
                vTcl:Toplevel:WidgetProc %W endmodal
            } else {
                destroy %W; if {$_topcount == 0} {exit}
            }
}
bind "_TopLevel" <Destroy> {
    if {[winfo toplevel %W] == "%W"} {incr _topcount -1}
}

Window show .
Window show .top37

