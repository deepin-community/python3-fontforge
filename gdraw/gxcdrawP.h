#ifndef FONTFORGE_GXCDRAWP_H
#define FONTFORGE_GXCDRAWP_H

#include <fontforge-config.h>

#ifndef FONTFORGE_CAN_USE_GDK

#include "gxdrawP.h"

extern int _GXCDraw_hasCairo(void);
#ifndef _NO_LIBCAIRO

extern void _GXCDraw_NewWindow(GXWindow nw);
extern void _GXCDraw_ResizeWindow(GXWindow gw,GRect *rect);
extern void _GXCDraw_DestroyWindow(GXWindow gw);

extern void _GXCDraw_PushClip(GXWindow gw);
extern void _GXCDraw_PopClip(GXWindow gw);
extern void _GXCDraw_PushClipOnly(GXWindow gw);
extern void _GXCDraw_ClipPreserve(GXWindow gw);

extern void _GXCDraw_Clear(GXWindow gw, GRect *rect);
extern void _GXCDraw_DrawLine(GXWindow gw, int32_t x,int32_t y, int32_t xend,int32_t yend);
extern void _GXCDraw_DrawArc(GXWindow gw, GRect *rect, double start_angle, double end_angle);
extern void _GXCDraw_DrawRect(GXWindow gw, GRect *rect);
extern void _GXCDraw_FillRect(GXWindow gw, GRect *rect);
extern void _GXCDraw_FillRoundRect(GXWindow gw, GRect *rect, int radius);
extern void _GXCDraw_DrawEllipse(GXWindow gw, GRect *rect);
extern void _GXCDraw_FillEllipse(GXWindow gw, GRect *rect);
extern void _GXCDraw_DrawPoly(GXWindow gw, GPoint *pts, int16_t cnt);
extern void _GXCDraw_FillPoly(GXWindow gw, GPoint *pts, int16_t cnt);

extern void _GXCDraw_Image( GXWindow gw, GImage *image, GRect *src, int32_t x, int32_t y);
extern void _GXCDraw_TileImage( GXWindow gw, GImage *image, GRect *src, int32_t x, int32_t y);
extern void _GXCDraw_Glyph( GXWindow gw, GImage *image, GRect *src, int32_t x, int32_t y);
extern void _GXCDraw_ImageMagnified(GXWindow gw, GImage *image, GRect *magsrc,
	int32_t x, int32_t y, int32_t width, int32_t height);
extern void _GXCDraw_CopyArea( GXWindow from, GXWindow into, GRect *src, int32_t x, int32_t y);

extern enum gcairo_flags _GXCDraw_CairoCapabilities( GXWindow );
extern void _GXCDraw_PathStartNew(GWindow w);
extern void _GXCDraw_PathStartSubNew(GWindow w);
extern int _GXCDraw_FillRuleSetWinding(GWindow w);
extern void _GXCDraw_PathClose(GWindow w);
extern void _GXCDraw_PathMoveTo(GWindow w,double x, double y);
extern void _GXCDraw_PathLineTo(GWindow w,double x, double y);
extern void _GXCDraw_PathCurveTo(GWindow w,
		    double cx1, double cy1,
		    double cx2, double cy2,
		    double x, double y);
extern void _GXCDraw_PathStroke(GWindow w,Color col);
extern void _GXCDraw_PathFill(GWindow w,Color col);
extern void _GXCDraw_PathFillAndStroke(GWindow w,Color fillcol, Color strokecol);

#include "fontP.h"
#endif
extern void _GXPDraw_NewWindow(GXWindow nw);
extern void _GXPDraw_DestroyWindow(GXWindow nw);
#include "fontP.h"
extern PangoFontDescription *_GXPDraw_configfont(GWindow gw, GFont *font);
extern int32_t _GXPDraw_DoText8(GWindow w, int32_t x, int32_t y,
	const char *text, int32_t cnt, Color col,
	enum text_funcs drawit, struct tf_arg *arg);
extern void _GXPDraw_FontMetrics(GWindow gw, GFont *fi, int *as, int *ds, int *ld);
extern void _GXPDraw_LayoutInit(GWindow w, char *text, int cnt, GFont *fi);
extern void _GXPDraw_LayoutDraw(GWindow w, int32_t x, int32_t y, Color fg);
extern void _GXPDraw_LayoutIndexToPos(GWindow w, int index, GRect *pos);
extern int  _GXPDraw_LayoutXYToIndex(GWindow w, int x, int y);
extern void _GXPDraw_LayoutExtents(GWindow w, GRect *size);
extern void _GXPDraw_LayoutSetWidth(GWindow w, int width);
extern int  _GXPDraw_LayoutLineCount(GWindow w);
extern int  _GXPDraw_LayoutLineStart(GWindow w,int l);

#endif /* FONTFORGE_CAN_USE_GDK */

#endif /* FONTFORGE_GXCDRAWP_H */
