### Windows 编译Kivy

#### 1.Why?
kivy 是python 框架解释型语言为什么要编译，那是因为kivy 底层的核心框架是C实现的，准确的说是cython 实现的，那说明是cython呢？[参考](demo/pyd_package/readme.md)

在windows 下 pip install 安装Kivy的时候的时候都是默认下载whl 包安装的， whl 包其实是zip的压缩包，whl 包在打包时候会根据不同的python环境和
位数在名称上标明，也就意味着whl 是环境强关联的不适用所以环境，最关键的是他内部的DLL 不带调试信息。所以在Kivy 应用崩溃的时候没法定位跟踪，需要自己
编译并保留pdb 调试信息

#### 2.编译环境
##### 2.1 Python 
python 目前选择[3.6.6版本](https://www.python.org/ftp/python/3.6.6/python-3.6.6.exe) ， 安装时候需要勾选调试信息包（pdb）和开发调
试包（lib和头文件）， 创建一个干净的python虚拟环境
[参考](https://zhuanlan.zhihu.com/p/60647332)

##### 2.2 C编译器
毫无疑问windows 应用编译肯定优先使用微软自带的Visual Studio VC++编译器，目前使用的python 版本是3.6.6 对应 [VS 2015社区版本](https://my.visualstudio.com/Downloads?q=visual%20studio%202015&wt.mc_id=o~msft~vscom~older-downloads) (VC14.0), 
cmd里输入python能查看对应编译器的版本
```shell
>python
Python 3.6.6 (v3.6.6:4cf1f54eb7, Jun 27 2018, 02:47:15) [MSC v.1900 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
安装过程略过。

#### 3.kivy源码 编译

下载源码 [Kivy2.0 ](https://github.com/kivy/kivy/releases/tag/2.0.0)是支持python3.6 的最高版本, 
kivy之所以强大，跨平台是因为core核心做了各个系统平台、场景所需的类库的适配，下面列出来的是核心库的依赖包。

##### 3.1 Kivy 图像依赖库
kivy 提供了多种图形渲染库的支持，有'glew', 'sdl2', 'gl', 'mock', 如果需要指定使用`KIVY_GL_BACKEND`环境变量配置, 具体说明参考
[CGL: standard C interface for OpenGL](https://kivy.org/doc/stable/api-kivy.graphics.cgl.html#module-kivy.graphics.cgl)


* 安装sdl2开发库`kivy-deps.sdl2_dev`（这里需要注意的是带`dev`的包）提供图像窗口相关的, 提供sdl2的lib库和头文件共编译使用，并没含dll 文件。
> pip install kivy-deps.sdl2      # 官方编译好的仅pyd(dll文件)
> pip install kivy-deps.sdl2_dev  # 官方编译好的lib 和lib 文件 

当使用SDL库时需要设置SDL2环境变量启用开关`SET USE_SDL2=1`，sdl2 提供了window窗口、贴图text、image图片、audio音频、clipboard粘贴板的功能,
windows 默认使用SDL 的底层图像库

* 安装glew开发库， 提供openGL的渲染接口，它能适配OpenGL 和OpenGL SE 等新老版本，被`kvy.graphics`模块引用(可选)
> pip install kivy-deps.glew      # 官方编译好的pyd(dll文件)
> pip install kivy-deps.glew_dev  # 官方编译好的lib 和lib 文件


* 安装angle开发库， 提供openGL的渲染接口，它是google在OpenGL SE之上封装的图图形，被`kvy.graphics`模块引用(可选)
> pip install kivy-deps.angle      # 官方编译好的pyd(dll文件)
~~> pip install kivy-deps.angle_dev  # 官方编译好的lib 和lib 文件~~ 2.0.0 没有使用


##### 3.2 视频依赖库
* 安装gstreamer开发库， 提供视频流的渲染接口，被`kvy.core.video`模块引用(可选), 这个库是基于glib写的，体积非常大110M左右
> pip install kivy-deps.gstreamer      # 官方编译好的pyd(dll文件)
> pip install kivy-deps.gstreamer_dev  # 官方编译好的lib 和lib 文件
 

##### 3.3 音频依赖库
音频流播放支持sdl2, gstplayer, ffpyplayer, pygame, avplayer几种库，除了sdl2其他都是python代码依赖，sdl已经覆盖所以安装略过


##### 3.4 摄像依赖库
kivy 支持avfoundation, android, opencv三种摄像库， `avfoundation` 用于ios需要编译pyx, 其他都不用编译


##### 3.5 粘贴板库
kivy 提供了sdl2, pygame, dummy, android四种库的实现，其中sdl2 是需要编译pyx的


#### 3.6 图片渲染库
支持sdl2, pil, pygame, imageio, tex, dds 几种方式渲染， 其中sdl2 是需要编译pyx的


##### 3.7 纹理贴图渲染库
支持sdl2, pil, pygame, sdlttf， 其中sdl2 是需要编译pyx的

##### 3.8 拼写检查库spelling
支持enchant, osxappkit 都是python 层级的代码，无需编译


##### 3.9 窗口框架库
窗口框架库提供主绘制区域和应用事件事件，支持sdl2, pygame, x11, egl_rpi， 其中sdl2、x11 是需要编译pyx的, x11 仅是unix操作系统体系下支持

> 上面pip 会自动命中当前python 支持的最高版本，也可以指定版本， 如果kivy-deps.sdl2_dev==2.0.12




##### 编译

kivy提供的setup.py 默认是不带pdb调试信息，需要修改setup.py源码，添加上release的pdb, `python setup.py --debug` 能编译从debug 版本的pdb
,但是python 都是release发不，所以只能自己动手需改源码了。 修改`KivyBuildExt.build_extensions`方法，位msvc编译器下添加连接器选项`/DEBUG:FULL`


```shell
class KivyBuildExt(build_ext, object):
  def build_extensions(self):
      # ...
      # ...
      print('Detected compiler is {}'.format(c))
      if c != 'msvc':
          for e in self.extensions:
              e.extra_link_args += ['-lm']
      else:
          for e in self.extensions:
              e.extra_link_args += ['/DEBUG:FULL']
```

设置sdl2开关位打开状态的环境变量`set use_sdl2=1`, 然后编译打包.whl包， `python setup.py bdist_wheel` 


```shell

(withPdbInfo) D:\workspace\Kivy-2.0.0>python setup.py build
sdl2 path:['C:\\Users\\guanglin.liang\\pythonEnv\\withPdbInfo\\share\\sdl2\\bin']
[INFO   ] [Logger      ] Record log in C:\Users\guanglin.liang\.kivy\logs\kivy_22-06-02_2.txt
[INFO   ] [deps        ] Successfully imported "kivy_deps.angle" 0.3.0
[INFO   ] [deps        ] Successfully imported "kivy_deps.glew" 0.3.0
[INFO   ] [deps        ] Successfully imported "kivy_deps.sdl2" 0.3.1
[INFO   ] [deps        ] Successfully imported "kivy_deps.sdl2_dev" 0.4.3
[INFO   ] [Kivy        ] v2.0.0
[INFO   ] [Kivy        ] Installed at "D:\workspace\Kivy-2.0.0\kivy\__init__.py"
[INFO   ] [Python      ] v3.6.6 (v3.6.6:4cf1f54eb7, Jun 27 2018, 02:47:15) [MSC v.1900 32 bit (Intel)]
[INFO   ] [Python      ] Interpreter at "C:\Users\guanglin.liang\pythonEnv\withPdbInfo\Scripts\python.exe"
Current directory is: D:\workspace\Kivy-2.0.0
Source and initial build directory is:
Python path is:
D:\workspace\Kivy-2.0.0
C:\Users\guanglin.liang\pythonEnv\withPdbInfo\Scripts\python36.zip
D:\tools\tools\python366-32with-pdb\DLLs
D:\tools\tools\python366-32with-pdb\lib
D:\tools\tools\python366-32with-pdb
C:\Users\guanglin.liang\pythonEnv\withPdbInfo
C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages
C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages\pypiwin32-223-py3.6.egg
C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages\pygments-2.12.0-py3.6.egg
C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages\docutils-0.18.1-py3.6.egg
C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages\cpython_example-0.0.1-py3.6-win32.egg
C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages\win32
C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages\win32\lib
C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages\Pythonwin
D:\workspace\Kivy-2.0.0\kivy\modules
C:\Users\guanglin.liang\.kivy\mods


Found Cython at C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages\Cython\__init__.py
Detected supported Cython version 0.29.19
User distribution detected, avoid portable command.
Using this graphics system: OpenGL
WARNING: A problem occurred while running pkg-config --libs --cflags gstreamer-1.0 (code 1)

b"'pkg-config' \xb2\xbb\xca\xc7\xc4\xda\xb2\xbf\xbb\xf2\xcd\xe2\xb2\xbf\xc3\xfc\xc1\xee\xa3\xac\xd2\xb2\xb2\xbb\xca\xc7\xbf\xc9\xd4\xcb\xd0\xd0\xb5\xc4\xb3\xcc\xd0\xf2\r\n\xbb\xf2\xc5\xfa\xb4\xa6\xc0\xed\xce\xc4\xbc\xfe\xa1\xa3\r\n"

WARNING: A problem occurred while running pkg-config --libs --cflags gstreamer-1.0 (code 1)

b"'pkg-config' \xb2\xbb\xca\xc7\xc4\xda\xb2\xbf\xbb\xf2\xcd\xe2\xb2\xbf\xc3\xfc\xc1\xee\xa3\xac\xd2\xb2\xb2\xbb\xca\xc7\xbf\xc9\xd4\xcb\xd0\xd0\xb5\xc4\xb3\xcc\xd0\xf2\r\n\xbb\xf2\xc5\xfa\xb4\xa6\xc0\xed\xce\xc4\xbc\xfe\xa1\xa3\r\n"

WARNING: A problem occurred while running pkg-config --libs --cflags sdl2 SDL2_ttf SDL2_image SDL2_mixer (code 1)

b"'pkg-config' \xb2\xbb\xca\xc7\xc4\xda\xb2\xbf\xbb\xf2\xcd\xe2\xb2\xbf\xc3\xfc\xc1\xee\xa3\xac\xd2\xb2\xb2\xbb\xca\xc7\xbf\xc9\xd4\xcb\xd0\xd0\xb5\xc4\xb3\xcc\xd0\xf2\r\n\xbb\xf2\xc5\xfa\xb4\xa6\xc0\xed\xce\xc4\xbc\xfe\xa1\xa3\r\n"

SDL2: found SDL header at C:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include\SDL2\SDL.h
SDL2: found SDL_mixer header at C:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include\SDL2\SDL_mixer.h
SDL2: found SDL_ttf header at C:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include\SDL2\SDL_ttf.h
SDL2: found SDL_image header at C:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include\SDL2\SDL_image.h
running build
running build_py
creating build
creating build\lib.win32-3.6
creating build\lib.win32-3.6\kivy
copying kivy\animation.py -> build\lib.win32-3.6\kivy
copying kivy\app.py -> build\lib.win32-3.6\kivy
copying kivy\atlas.py -> build\lib.win32-3.6\kivy
copying kivy\base.py -> build\lib.win32-3.6\kivy
copying kivy\cache.py -> build\lib.win32-3.6\kivy
copying kivy\clock.py -> build\lib.win32-3.6\kivy
copying kivy\compat.py -> build\lib.win32-3.6\kivy
copying kivy\config.py -> build\lib.win32-3.6\kivy
copying kivy\context.py -> build\lib.win32-3.6\kivy
copying kivy\event.py -> build\lib.win32-3.6\kivy
copying kivy\factory.py -> build\lib.win32-3.6\kivy
copying kivy\factory_registers.py -> build\lib.win32-3.6\kivy
copying kivy\geometry.py -> build\lib.win32-3.6\kivy
copying kivy\gesture.py -> build\lib.win32-3.6\kivy
copying kivy\interactive.py -> build\lib.win32-3.6\kivy
copying kivy\loader.py -> build\lib.win32-3.6\kivy
copying kivy\logger.py -> build\lib.win32-3.6\kivy
copying kivy\metrics.py -> build\lib.win32-3.6\kivy
copying kivy\multistroke.py -> build\lib.win32-3.6\kivy
copying kivy\parser.py -> build\lib.win32-3.6\kivy
copying kivy\resources.py -> build\lib.win32-3.6\kivy
copying kivy\setupconfig.py -> build\lib.win32-3.6\kivy
copying kivy\support.py -> build\lib.win32-3.6\kivy
copying kivy\utils.py -> build\lib.win32-3.6\kivy
copying kivy\vector.py -> build\lib.win32-3.6\kivy
copying kivy\weakmethod.py -> build\lib.win32-3.6\kivy
copying kivy\_version.py -> build\lib.win32-3.6\kivy
copying kivy\__init__.py -> build\lib.win32-3.6\kivy
creating build\lib.win32-3.6\kivy\core
copying kivy\core\__init__.py -> build\lib.win32-3.6\kivy\core
creating build\lib.win32-3.6\kivy\deps
copying kivy\deps\__init__.py -> build\lib.win32-3.6\kivy\deps
creating build\lib.win32-3.6\kivy\effects
copying kivy\effects\dampedscroll.py -> build\lib.win32-3.6\kivy\effects
copying kivy\effects\kinetic.py -> build\lib.win32-3.6\kivy\effects
copying kivy\effects\opacityscroll.py -> build\lib.win32-3.6\kivy\effects
copying kivy\effects\scroll.py -> build\lib.win32-3.6\kivy\effects
copying kivy\effects\__init__.py -> build\lib.win32-3.6\kivy\effects
creating build\lib.win32-3.6\kivy\extras
copying kivy\extras\highlight.py -> build\lib.win32-3.6\kivy\extras
copying kivy\extras\__init__.py -> build\lib.win32-3.6\kivy\extras
creating build\lib.win32-3.6\kivy\garden
copying kivy\garden\__init__.py -> build\lib.win32-3.6\kivy\garden
creating build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\__init__.py -> build\lib.win32-3.6\kivy\graphics
creating build\lib.win32-3.6\kivy\input
copying kivy\input\factory.py -> build\lib.win32-3.6\kivy\input
copying kivy\input\motionevent.py -> build\lib.win32-3.6\kivy\input
copying kivy\input\provider.py -> build\lib.win32-3.6\kivy\input
copying kivy\input\recorder.py -> build\lib.win32-3.6\kivy\input
copying kivy\input\shape.py -> build\lib.win32-3.6\kivy\input
copying kivy\input\__init__.py -> build\lib.win32-3.6\kivy\input
creating build\lib.win32-3.6\kivy\lang
copying kivy\lang\builder.py -> build\lib.win32-3.6\kivy\lang
copying kivy\lang\parser.py -> build\lib.win32-3.6\kivy\lang
copying kivy\lang\__init__.py -> build\lib.win32-3.6\kivy\lang
creating build\lib.win32-3.6\kivy\lib
copying kivy\lib\ddsfile.py -> build\lib.win32-3.6\kivy\lib
copying kivy\lib\mtdev.py -> build\lib.win32-3.6\kivy\lib
copying kivy\lib\__init__.py -> build\lib.win32-3.6\kivy\lib
creating build\lib.win32-3.6\kivy\modules
copying kivy\modules\console.py -> build\lib.win32-3.6\kivy\modules
copying kivy\modules\cursor.py -> build\lib.win32-3.6\kivy\modules
copying kivy\modules\inspector.py -> build\lib.win32-3.6\kivy\modules
copying kivy\modules\joycursor.py -> build\lib.win32-3.6\kivy\modules
copying kivy\modules\keybinding.py -> build\lib.win32-3.6\kivy\modules
copying kivy\modules\monitor.py -> build\lib.win32-3.6\kivy\modules
copying kivy\modules\recorder.py -> build\lib.win32-3.6\kivy\modules
copying kivy\modules\screen.py -> build\lib.win32-3.6\kivy\modules
copying kivy\modules\showborder.py -> build\lib.win32-3.6\kivy\modules
copying kivy\modules\touchring.py -> build\lib.win32-3.6\kivy\modules
copying kivy\modules\webdebugger.py -> build\lib.win32-3.6\kivy\modules
copying kivy\modules\_webdebugger.py -> build\lib.win32-3.6\kivy\modules
copying kivy\modules\__init__.py -> build\lib.win32-3.6\kivy\modules
creating build\lib.win32-3.6\kivy\network
copying kivy\network\urlrequest.py -> build\lib.win32-3.6\kivy\network
copying kivy\network\__init__.py -> build\lib.win32-3.6\kivy\network
creating build\lib.win32-3.6\kivy\storage
copying kivy\storage\dictstore.py -> build\lib.win32-3.6\kivy\storage
copying kivy\storage\jsonstore.py -> build\lib.win32-3.6\kivy\storage
copying kivy\storage\redisstore.py -> build\lib.win32-3.6\kivy\storage
copying kivy\storage\__init__.py -> build\lib.win32-3.6\kivy\storage
creating build\lib.win32-3.6\kivy\tests
copying kivy\tests\async_common.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\common.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\conftest.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\fixtures.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\perf_test_textinput.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_animations.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_app.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_audio.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_clipboard.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_clock.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_coverage.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_doc_gallery.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_fbo_py2py3.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_filechooser.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_filechooser_unicode.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_fonts.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_graphics.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_image.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_imageloader.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_invalid_lang.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_knspace.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_lang.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_lang_complex.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_lang_pre_process_and_post_process.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_module_inspector.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_mouse_multitouchsim.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_multistroke.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_properties.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_rst_replace.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_screen.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_storage.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_uix_actionbar.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_uix_anchorlayout.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_uix_asyncimage.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_uix_boxlayout.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_uix_bubble.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_uix_carousel.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_uix_dropdown.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_uix_gridlayout.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_uix_layout.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_uix_modal.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_uix_relativelayout.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_uix_scrollview.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_uix_slider.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_uix_stacklayout.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_uix_textinput.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_uix_translate_coordinates.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_uix_widget.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_urlrequest.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_utils.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_vector.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_video.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_weakmethod.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_widget.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_widget_walk.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_window_info.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\visual_test_label.py -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\__init__.py -> build\lib.win32-3.6\kivy\tests
creating build\lib.win32-3.6\kivy\tools
copying kivy\tools\benchmark.py -> build\lib.win32-3.6\kivy\tools
copying kivy\tools\changelog_parser.py -> build\lib.win32-3.6\kivy\tools
copying kivy\tools\coverage.py -> build\lib.win32-3.6\kivy\tools
copying kivy\tools\gallery.py -> build\lib.win32-3.6\kivy\tools
copying kivy\tools\generate-icons.py -> build\lib.win32-3.6\kivy\tools
copying kivy\tools\kviewer.py -> build\lib.win32-3.6\kivy\tools
copying kivy\tools\report.py -> build\lib.win32-3.6\kivy\tools
copying kivy\tools\stub-gl-debug.py -> build\lib.win32-3.6\kivy\tools
copying kivy\tools\texturecompress.py -> build\lib.win32-3.6\kivy\tools
copying kivy\tools\__init__.py -> build\lib.win32-3.6\kivy\tools
creating build\lib.win32-3.6\kivy\uix
copying kivy\uix\accordion.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\actionbar.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\anchorlayout.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\boxlayout.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\bubble.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\button.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\camera.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\carousel.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\checkbox.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\codeinput.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\colorpicker.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\dropdown.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\effectwidget.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\filechooser.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\floatlayout.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\gesturesurface.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\gridlayout.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\image.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\label.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\layout.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\modalview.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\pagelayout.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\popup.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\progressbar.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\recycleboxlayout.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\recyclegridlayout.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\recyclelayout.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\relativelayout.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\rst.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\sandbox.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\scatter.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\scatterlayout.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\screenmanager.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\scrollview.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\settings.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\slider.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\spinner.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\splitter.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\stacklayout.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\stencilview.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\switch.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\tabbedpanel.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\textinput.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\togglebutton.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\treeview.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\video.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\videoplayer.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\vkeyboard.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\widget.py -> build\lib.win32-3.6\kivy\uix
copying kivy\uix\__init__.py -> build\lib.win32-3.6\kivy\uix
creating build\lib.win32-3.6\kivy\core\audio
copying kivy\core\audio\audio_android.py -> build\lib.win32-3.6\kivy\core\audio
copying kivy\core\audio\audio_avplayer.py -> build\lib.win32-3.6\kivy\core\audio
copying kivy\core\audio\audio_ffpyplayer.py -> build\lib.win32-3.6\kivy\core\audio
copying kivy\core\audio\audio_gstplayer.py -> build\lib.win32-3.6\kivy\core\audio
copying kivy\core\audio\audio_pygame.py -> build\lib.win32-3.6\kivy\core\audio
copying kivy\core\audio\__init__.py -> build\lib.win32-3.6\kivy\core\audio
creating build\lib.win32-3.6\kivy\core\camera
copying kivy\core\camera\camera_android.py -> build\lib.win32-3.6\kivy\core\camera
copying kivy\core\camera\camera_gi.py -> build\lib.win32-3.6\kivy\core\camera
copying kivy\core\camera\camera_opencv.py -> build\lib.win32-3.6\kivy\core\camera
copying kivy\core\camera\camera_picamera.py -> build\lib.win32-3.6\kivy\core\camera
copying kivy\core\camera\__init__.py -> build\lib.win32-3.6\kivy\core\camera
creating build\lib.win32-3.6\kivy\core\clipboard
copying kivy\core\clipboard\clipboard_android.py -> build\lib.win32-3.6\kivy\core\clipboard
copying kivy\core\clipboard\clipboard_dbusklipper.py -> build\lib.win32-3.6\kivy\core\clipboard
copying kivy\core\clipboard\clipboard_dummy.py -> build\lib.win32-3.6\kivy\core\clipboard
copying kivy\core\clipboard\clipboard_gtk3.py -> build\lib.win32-3.6\kivy\core\clipboard
copying kivy\core\clipboard\clipboard_nspaste.py -> build\lib.win32-3.6\kivy\core\clipboard
copying kivy\core\clipboard\clipboard_pygame.py -> build\lib.win32-3.6\kivy\core\clipboard
copying kivy\core\clipboard\clipboard_sdl2.py -> build\lib.win32-3.6\kivy\core\clipboard
copying kivy\core\clipboard\clipboard_winctypes.py -> build\lib.win32-3.6\kivy\core\clipboard
copying kivy\core\clipboard\clipboard_xclip.py -> build\lib.win32-3.6\kivy\core\clipboard
copying kivy\core\clipboard\clipboard_xsel.py -> build\lib.win32-3.6\kivy\core\clipboard
copying kivy\core\clipboard\_clipboard_ext.py -> build\lib.win32-3.6\kivy\core\clipboard
copying kivy\core\clipboard\__init__.py -> build\lib.win32-3.6\kivy\core\clipboard
creating build\lib.win32-3.6\kivy\core\gl
copying kivy\core\gl\__init__.py -> build\lib.win32-3.6\kivy\core\gl
creating build\lib.win32-3.6\kivy\core\image
copying kivy\core\image\img_dds.py -> build\lib.win32-3.6\kivy\core\image
copying kivy\core\image\img_ffpyplayer.py -> build\lib.win32-3.6\kivy\core\image
copying kivy\core\image\img_pil.py -> build\lib.win32-3.6\kivy\core\image
copying kivy\core\image\img_pygame.py -> build\lib.win32-3.6\kivy\core\image
copying kivy\core\image\img_sdl2.py -> build\lib.win32-3.6\kivy\core\image
copying kivy\core\image\img_tex.py -> build\lib.win32-3.6\kivy\core\image
copying kivy\core\image\__init__.py -> build\lib.win32-3.6\kivy\core\image
creating build\lib.win32-3.6\kivy\core\spelling
copying kivy\core\spelling\spelling_enchant.py -> build\lib.win32-3.6\kivy\core\spelling
copying kivy\core\spelling\spelling_osxappkit.py -> build\lib.win32-3.6\kivy\core\spelling
copying kivy\core\spelling\__init__.py -> build\lib.win32-3.6\kivy\core\spelling
creating build\lib.win32-3.6\kivy\core\text
copying kivy\core\text\markup.py -> build\lib.win32-3.6\kivy\core\text
copying kivy\core\text\text_pango.py -> build\lib.win32-3.6\kivy\core\text
copying kivy\core\text\text_pil.py -> build\lib.win32-3.6\kivy\core\text
copying kivy\core\text\text_pygame.py -> build\lib.win32-3.6\kivy\core\text
copying kivy\core\text\text_sdl2.py -> build\lib.win32-3.6\kivy\core\text
copying kivy\core\text\__init__.py -> build\lib.win32-3.6\kivy\core\text
creating build\lib.win32-3.6\kivy\core\video
copying kivy\core\video\video_ffmpeg.py -> build\lib.win32-3.6\kivy\core\video
copying kivy\core\video\video_ffpyplayer.py -> build\lib.win32-3.6\kivy\core\video
copying kivy\core\video\video_gstplayer.py -> build\lib.win32-3.6\kivy\core\video
copying kivy\core\video\video_null.py -> build\lib.win32-3.6\kivy\core\video
copying kivy\core\video\__init__.py -> build\lib.win32-3.6\kivy\core\video
creating build\lib.win32-3.6\kivy\core\window
copying kivy\core\window\window_egl_rpi.py -> build\lib.win32-3.6\kivy\core\window
copying kivy\core\window\window_pygame.py -> build\lib.win32-3.6\kivy\core\window
copying kivy\core\window\window_sdl2.py -> build\lib.win32-3.6\kivy\core\window
copying kivy\core\window\__init__.py -> build\lib.win32-3.6\kivy\core\window
creating build\lib.win32-3.6\kivy\graphics\cgl_backend
copying kivy\graphics\cgl_backend\__init__.py -> build\lib.win32-3.6\kivy\graphics\cgl_backend
creating build\lib.win32-3.6\kivy\input\postproc
copying kivy\input\postproc\calibration.py -> build\lib.win32-3.6\kivy\input\postproc
copying kivy\input\postproc\dejitter.py -> build\lib.win32-3.6\kivy\input\postproc
copying kivy\input\postproc\doubletap.py -> build\lib.win32-3.6\kivy\input\postproc
copying kivy\input\postproc\ignorelist.py -> build\lib.win32-3.6\kivy\input\postproc
copying kivy\input\postproc\retaintouch.py -> build\lib.win32-3.6\kivy\input\postproc
copying kivy\input\postproc\tripletap.py -> build\lib.win32-3.6\kivy\input\postproc
copying kivy\input\postproc\__init__.py -> build\lib.win32-3.6\kivy\input\postproc
creating build\lib.win32-3.6\kivy\input\providers
copying kivy\input\providers\androidjoystick.py -> build\lib.win32-3.6\kivy\input\providers
copying kivy\input\providers\hidinput.py -> build\lib.win32-3.6\kivy\input\providers
copying kivy\input\providers\leapfinger.py -> build\lib.win32-3.6\kivy\input\providers
copying kivy\input\providers\linuxwacom.py -> build\lib.win32-3.6\kivy\input\providers
copying kivy\input\providers\mactouch.py -> build\lib.win32-3.6\kivy\input\providers
copying kivy\input\providers\mouse.py -> build\lib.win32-3.6\kivy\input\providers
copying kivy\input\providers\mtdev.py -> build\lib.win32-3.6\kivy\input\providers
copying kivy\input\providers\probesysfs.py -> build\lib.win32-3.6\kivy\input\providers
copying kivy\input\providers\tuio.py -> build\lib.win32-3.6\kivy\input\providers
copying kivy\input\providers\wm_common.py -> build\lib.win32-3.6\kivy\input\providers
copying kivy\input\providers\wm_pen.py -> build\lib.win32-3.6\kivy\input\providers
copying kivy\input\providers\wm_touch.py -> build\lib.win32-3.6\kivy\input\providers
copying kivy\input\providers\__init__.py -> build\lib.win32-3.6\kivy\input\providers
creating build\lib.win32-3.6\kivy\lib\gstplayer
copying kivy\lib\gstplayer\__init__.py -> build\lib.win32-3.6\kivy\lib\gstplayer
creating build\lib.win32-3.6\kivy\lib\vidcore_lite
copying kivy\lib\vidcore_lite\__init__.py -> build\lib.win32-3.6\kivy\lib\vidcore_lite
creating build\lib.win32-3.6\kivy\tools\highlight
copying kivy\tools\highlight\__init__.py -> build\lib.win32-3.6\kivy\tools\highlight
creating build\lib.win32-3.6\kivy\tools\packaging
copying kivy\tools\packaging\cython_cfg.py -> build\lib.win32-3.6\kivy\tools\packaging
copying kivy\tools\packaging\factory.py -> build\lib.win32-3.6\kivy\tools\packaging
copying kivy\tools\packaging\__init__.py -> build\lib.win32-3.6\kivy\tools\packaging
creating build\lib.win32-3.6\kivy\tools\packaging\pyinstaller_hooks
copying kivy\tools\packaging\pyinstaller_hooks\hook-kivy.py -> build\lib.win32-3.6\kivy\tools\packaging\pyinstaller_hooks
copying kivy\tools\packaging\pyinstaller_hooks\pyi_rth_kivy.py -> build\lib.win32-3.6\kivy\tools\packaging\pyinstaller_hooks
copying kivy\tools\packaging\pyinstaller_hooks\__init__.py -> build\lib.win32-3.6\kivy\tools\packaging\pyinstaller_hooks
copying kivy\tools\packaging\pyinstaller_hooks\__main__.py -> build\lib.win32-3.6\kivy\tools\packaging\pyinstaller_hooks
creating build\lib.win32-3.6\kivy\uix\behaviors
copying kivy\uix\behaviors\button.py -> build\lib.win32-3.6\kivy\uix\behaviors
copying kivy\uix\behaviors\codenavigation.py -> build\lib.win32-3.6\kivy\uix\behaviors
copying kivy\uix\behaviors\compoundselection.py -> build\lib.win32-3.6\kivy\uix\behaviors
copying kivy\uix\behaviors\cover.py -> build\lib.win32-3.6\kivy\uix\behaviors
copying kivy\uix\behaviors\drag.py -> build\lib.win32-3.6\kivy\uix\behaviors
copying kivy\uix\behaviors\emacs.py -> build\lib.win32-3.6\kivy\uix\behaviors
copying kivy\uix\behaviors\focus.py -> build\lib.win32-3.6\kivy\uix\behaviors
copying kivy\uix\behaviors\knspace.py -> build\lib.win32-3.6\kivy\uix\behaviors
copying kivy\uix\behaviors\togglebutton.py -> build\lib.win32-3.6\kivy\uix\behaviors
copying kivy\uix\behaviors\touchripple.py -> build\lib.win32-3.6\kivy\uix\behaviors
copying kivy\uix\behaviors\__init__.py -> build\lib.win32-3.6\kivy\uix\behaviors
creating build\lib.win32-3.6\kivy\uix\recycleview
copying kivy\uix\recycleview\datamodel.py -> build\lib.win32-3.6\kivy\uix\recycleview
copying kivy\uix\recycleview\layout.py -> build\lib.win32-3.6\kivy\uix\recycleview
copying kivy\uix\recycleview\views.py -> build\lib.win32-3.6\kivy\uix\recycleview
copying kivy\uix\recycleview\__init__.py -> build\lib.win32-3.6\kivy\uix\recycleview
copying kivy\properties.pxd -> build\lib.win32-3.6\kivy
copying kivy\_clock.pxd -> build\lib.win32-3.6\kivy
copying kivy\_event.pxd -> build\lib.win32-3.6\kivy
copying kivy\core\text\text_layout.pxd -> build\lib.win32-3.6\kivy\core\text
copying kivy\core\window\window_info.pxd -> build\lib.win32-3.6\kivy\core\window
copying kivy\graphics\buffer.pxd -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\cgl.pxd -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\compiler.pxd -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\context.pxd -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\context_instructions.pxd -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\fbo.pxd -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\instructions.pxd -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\opengl_utils.pxd -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\shader.pxd -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\stencil_instructions.pxd -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\svg.pxd -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\tesselator.pxd -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\texture.pxd -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\transformation.pxd -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\vbo.pxd -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\vertex.pxd -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\vertex_instructions.pxd -> build\lib.win32-3.6\kivy\graphics
copying kivy\lib\vidcore_lite\bcm.pxd -> build\lib.win32-3.6\kivy\lib\vidcore_lite
copying kivy\core\window\window_attrs.pxi -> build\lib.win32-3.6\kivy\core\window
copying kivy\graphics\common.pxi -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\gl_debug_logger.pxi -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\img_tools.pxi -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\memory.pxi -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\opcodes.pxi -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\opengl_utils_def.pxi -> build\lib.win32-3.6\kivy\graphics
copying kivy\graphics\vertex_instructions_line.pxi -> build\lib.win32-3.6\kivy\graphics
creating build\lib.win32-3.6\kivy\include
copying kivy\include\config.pxi -> build\lib.win32-3.6\kivy\include
copying kivy\lib\sdl2.pxi -> build\lib.win32-3.6\kivy\lib
creating build\lib.win32-3.6\kivy\lib\pango
copying kivy\lib\pango\pangoft2.pxi -> build\lib.win32-3.6\kivy\lib\pango
creating build\lib.win32-3.6\kivy\data
copying kivy\data\settings_kivy.json -> build\lib.win32-3.6\kivy\data
copying kivy\data\style.kv -> build\lib.win32-3.6\kivy\data
creating build\lib.win32-3.6\kivy\data\fonts
copying kivy\data\fonts\DejaVuSans.ttf -> build\lib.win32-3.6\kivy\data\fonts
copying kivy\data\fonts\Roboto-Bold.ttf -> build\lib.win32-3.6\kivy\data\fonts
copying kivy\data\fonts\Roboto-BoldItalic.ttf -> build\lib.win32-3.6\kivy\data\fonts
copying kivy\data\fonts\Roboto-Italic.ttf -> build\lib.win32-3.6\kivy\data\fonts
copying kivy\data\fonts\Roboto-Regular.ttf -> build\lib.win32-3.6\kivy\data\fonts
copying kivy\data\fonts\RobotoMono-Regular.ttf -> build\lib.win32-3.6\kivy\data\fonts
creating build\lib.win32-3.6\kivy\data\glsl
copying kivy\data\glsl\default.fs -> build\lib.win32-3.6\kivy\data\glsl
copying kivy\data\glsl\default.png -> build\lib.win32-3.6\kivy\data\glsl
copying kivy\data\glsl\default.vs -> build\lib.win32-3.6\kivy\data\glsl
copying kivy\data\glsl\header.fs -> build\lib.win32-3.6\kivy\data\glsl
copying kivy\data\glsl\header.vs -> build\lib.win32-3.6\kivy\data\glsl
creating build\lib.win32-3.6\kivy\data\images
copying kivy\data\images\background.jpg -> build\lib.win32-3.6\kivy\data\images
copying kivy\data\images\cursor.png -> build\lib.win32-3.6\kivy\data\images
copying kivy\data\images\defaultshape.png -> build\lib.win32-3.6\kivy\data\images
copying kivy\data\images\defaulttheme-0.png -> build\lib.win32-3.6\kivy\data\images
copying kivy\data\images\defaulttheme.atlas -> build\lib.win32-3.6\kivy\data\images
copying kivy\data\images\image-loading.gif -> build\lib.win32-3.6\kivy\data\images
copying kivy\data\images\image-loading.zip -> build\lib.win32-3.6\kivy\data\images
copying kivy\data\images\testpattern.png -> build\lib.win32-3.6\kivy\data\images
creating build\lib.win32-3.6\kivy\data\keyboards
copying kivy\data\keyboards\azerty.json -> build\lib.win32-3.6\kivy\data\keyboards
copying kivy\data\keyboards\de.json -> build\lib.win32-3.6\kivy\data\keyboards
copying kivy\data\keyboards\de_CH.json -> build\lib.win32-3.6\kivy\data\keyboards
copying kivy\data\keyboards\en_US.json -> build\lib.win32-3.6\kivy\data\keyboards
copying kivy\data\keyboards\fr_CH.json -> build\lib.win32-3.6\kivy\data\keyboards
copying kivy\data\keyboards\qwerty.json -> build\lib.win32-3.6\kivy\data\keyboards
copying kivy\data\keyboards\qwertz.json -> build\lib.win32-3.6\kivy\data\keyboards
creating build\lib.win32-3.6\kivy\data\logo
copying kivy\data\logo\kivy-icon-128.png -> build\lib.win32-3.6\kivy\data\logo
copying kivy\data\logo\kivy-icon-16.png -> build\lib.win32-3.6\kivy\data\logo
copying kivy\data\logo\kivy-icon-24.png -> build\lib.win32-3.6\kivy\data\logo
copying kivy\data\logo\kivy-icon-256.png -> build\lib.win32-3.6\kivy\data\logo
copying kivy\data\logo\kivy-icon-32.png -> build\lib.win32-3.6\kivy\data\logo
copying kivy\data\logo\kivy-icon-48.png -> build\lib.win32-3.6\kivy\data\logo
copying kivy\data\logo\kivy-icon-512.png -> build\lib.win32-3.6\kivy\data\logo
copying kivy\data\logo\kivy-icon-64.ico -> build\lib.win32-3.6\kivy\data\logo
copying kivy\data\logo\kivy-icon-64.png -> build\lib.win32-3.6\kivy\data\logo
copying kivy\include\common_subset.h -> build\lib.win32-3.6\kivy\include
copying kivy\include\config.h -> build\lib.win32-3.6\kivy\include
copying kivy\include\gl2platform.h -> build\lib.win32-3.6\kivy\include
copying kivy\include\gl_redirect.h -> build\lib.win32-3.6\kivy\include
copying kivy\include\khrplatform.h -> build\lib.win32-3.6\kivy\include
creating build\lib.win32-3.6\kivy\tools\gles_compat
copying kivy\tools\gles_compat\gl2.h -> build\lib.win32-3.6\kivy\tools\gles_compat
copying kivy\tools\gles_compat\subset_gles.py -> build\lib.win32-3.6\kivy\tools\gles_compat
copying kivy\tools\highlight\kivy-mode.el -> build\lib.win32-3.6\kivy\tools\highlight
copying kivy\tools\highlight\kivy.json-tmlanguage -> build\lib.win32-3.6\kivy\tools\highlight
copying kivy\tools\highlight\kivy.tmLanguage -> build\lib.win32-3.6\kivy\tools\highlight
copying kivy\tools\highlight\kivy.vim -> build\lib.win32-3.6\kivy\tools\highlight
creating build\lib.win32-3.6\kivy\tools\image-testsuite
copying kivy\tools\image-testsuite\gimp28-testsuite.py -> build\lib.win32-3.6\kivy\tools\image-testsuite
copying kivy\tools\image-testsuite\imagemagick-testsuite.sh -> build\lib.win32-3.6\kivy\tools\image-testsuite
copying kivy\tools\image-testsuite\README.md -> build\lib.win32-3.6\kivy\tools\image-testsuite
creating build\lib.win32-3.6\kivy\tools\pep8checker
copying kivy\tools\pep8checker\pep8.py -> build\lib.win32-3.6\kivy\tools\pep8checker
copying kivy\tools\pep8checker\pep8kivy.py -> build\lib.win32-3.6\kivy\tools\pep8checker
copying kivy\tools\pep8checker\pre-commit.githook -> build\lib.win32-3.6\kivy\tools\pep8checker
creating build\lib.win32-3.6\kivy\tools\theming
creating build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\action_bar.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\action_group.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\action_group_disabled.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\action_group_down.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\action_item.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\action_item_down.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\action_view.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\audio-volume-high.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\audio-volume-low.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\audio-volume-medium.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\audio-volume-muted.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\bubble.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\bubble_arrow.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\bubble_btn.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\bubble_btn_pressed.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\button.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\button_disabled.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\button_disabled_pressed.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\button_pressed.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\checkbox_disabled_off.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\checkbox_disabled_on.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\checkbox_off.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\checkbox_on.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\checkbox_radio_disabled_off.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\checkbox_radio_disabled_on.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\checkbox_radio_off.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\checkbox_radio_on.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\close.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\filechooser_file.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\filechooser_folder.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\filechooser_selected.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\image-missing.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\media-playback-pause.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\media-playback-start.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\media-playback-stop.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\modalview-background.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\overflow.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\player-background.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\player-play-overlay.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\previous_normal.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\progressbar.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\progressbar_background.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\ring.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\selector_left.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\selector_middle.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\selector_right.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\separator.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\sliderh_background.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\sliderh_background_disabled.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\sliderv_background.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\sliderv_background_disabled.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\slider_cursor.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\slider_cursor_disabled.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\spinner.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\spinner_disabled.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\spinner_pressed.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\splitter.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\splitter_disabled.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\splitter_disabled_down.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\splitter_disabled_down_h.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\splitter_disabled_h.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\splitter_down.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\splitter_down_h.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\splitter_grip.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\splitter_grip_h.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\splitter_h.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\switch-background.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\switch-background_disabled.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\switch-button.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\switch-button_disabled.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\tab.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\tab_btn.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\tab_btn_disabled.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\tab_btn_disabled_pressed.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\tab_btn_pressed.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\tab_disabled.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\textinput.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\textinput_active.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\textinput_disabled.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\textinput_disabled_active.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\tree_closed.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\tree_opened.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\vkeyboard_background.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\vkeyboard_disabled_background.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\vkeyboard_disabled_key_down.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\vkeyboard_disabled_key_normal.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\vkeyboard_key_down.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tools\theming\defaulttheme\vkeyboard_key_normal.png -> build\lib.win32-3.6\kivy\tools\theming\defaulttheme
copying kivy\tests\coverage_lang.kv -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\sample1.ogg -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\testkv.kv -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\test_button.png -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\unicode_files.zip -> build\lib.win32-3.6\kivy\tests
copying kivy\tests\unicode_font.zip -> build\lib.win32-3.6\kivy\tests
creating build\lib.win32-3.6\kivy\tests\pyinstaller
copying kivy\tests\pyinstaller\test_pyinstaller.py -> build\lib.win32-3.6\kivy\tests\pyinstaller
creating build\lib.win32-3.6\kivy\tests\pyinstaller\simple_widget
copying kivy\tests\pyinstaller\simple_widget\main.py -> build\lib.win32-3.6\kivy\tests\pyinstaller\simple_widget
copying kivy\tests\pyinstaller\simple_widget\main.spec -> build\lib.win32-3.6\kivy\tests\pyinstaller\simple_widget
creating build\lib.win32-3.6\kivy\tests\pyinstaller\simple_widget\project
copying kivy\tests\pyinstaller\simple_widget\project\widget.py -> build\lib.win32-3.6\kivy\tests\pyinstaller\simple_widget\project
copying kivy\tests\pyinstaller\simple_widget\project\__init__.py -> build\lib.win32-3.6\kivy\tests\pyinstaller\simple_widget\project
creating build\lib.win32-3.6\kivy\tests\pyinstaller\video_widget
copying kivy\tests\pyinstaller\video_widget\main.py -> build\lib.win32-3.6\kivy\tests\pyinstaller\video_widget
copying kivy\tests\pyinstaller\video_widget\main.spec -> build\lib.win32-3.6\kivy\tests\pyinstaller\video_widget
creating build\lib.win32-3.6\kivy\tests\pyinstaller\video_widget\project
copying kivy\tests\pyinstaller\video_widget\project\__init__.py -> build\lib.win32-3.6\kivy\tests\pyinstaller\video_widget\project
creating build\lib.win32-3.6\kivy\tests\test_issues
copying kivy\tests\test_issues\test_6315.py -> build\lib.win32-3.6\kivy\tests\test_issues
copying kivy\tests\test_issues\test_issue_1084.py -> build\lib.win32-3.6\kivy\tests\test_issues
copying kivy\tests\test_issues\test_issue_1091.py -> build\lib.win32-3.6\kivy\tests\test_issues
copying kivy\tests\test_issues\test_issue_599.py -> build\lib.win32-3.6\kivy\tests\test_issues
copying kivy\tests\test_issues\test_issue_609.py -> build\lib.win32-3.6\kivy\tests\test_issues
copying kivy\tests\test_issues\test_issue_6909.py -> build\lib.win32-3.6\kivy\tests\test_issues
copying kivy\tests\test_issues\test_issue_883.py -> build\lib.win32-3.6\kivy\tests\test_issues
running build_ext
Building extensions in parallel using 4 cores
Updated build directory to: build\lib.win32-3.6
Build configuration is:
 * use_rpi = 0
 * use_egl = 0
 * use_opengl_es2 = 0
 * use_opengl_mock = 0
 * use_sdl2 = 1
 * use_pangoft2 = 0
 * use_ios = 0
 * use_android = 0
 * use_mesagl = 0
 * use_x11 = 0
 * use_wayland = 0
 * use_gstreamer = 0
 * use_avfoundation = 0
 * use_osx_frameworks = 0
 * debug_gl = 0
 * kivy_sdl_gl_alpha_size = 8
 * debug = False
Detected compiler is msvc
skipping 'kivy\_event.c' Cython extension (up-to-date)
skipping 'kivy\_clock.c' Cython extension (up-to-date)
skipping 'kivy\weakproxy.c' Cython extension (up-to-date)
skipping 'kivy\properties.c' Cython extension (up-to-date)
skipping 'kivy\graphics\buffer.c' Cython extension (up-to-date)
skipping 'kivy\graphics\context.c' Cython extension (up-to-date)
skipping 'kivy\graphics\compiler.c' Cython extension (up-to-date)
skipping 'kivy\graphics\context_instructions.c' Cython extension (up-to-date)
skipping 'kivy\graphics\fbo.c' Cython extension (up-to-date)
skipping 'kivy\graphics\gl_instructions.c' Cython extension (up-to-date)
skipping 'kivy\graphics\instructions.c' Cython extension (up-to-date)
skipping 'kivy\graphics\opengl.c' Cython extension (up-to-date)
skipping 'kivy\graphics\opengl_utils.c' Cython extension (up-to-date)
skipping 'kivy\graphics\shader.c' Cython extension (up-to-date)
skipping 'kivy\graphics\stencil_instructions.c' Cython extension (up-to-date)
skipping 'kivy\graphics\scissor_instructions.c' Cython extension (up-to-date)
skipping 'kivy\graphics\texture.c' Cython extension (up-to-date)
skipping 'kivy\graphics\transformation.c' Cython extension (up-to-date)
skipping 'kivy\graphics\vbo.c' Cython extension (up-to-date)
skipping 'kivy\graphics\vertex.c' Cython extension (up-to-date)
skipping 'kivy\graphics\vertex_instructions.c' Cython extension (up-to-date)
skipping 'kivy\graphics\cgl.c' Cython extension (up-to-date)
skipping 'kivy\graphics/cgl_backend\cgl_mock.c' Cython extension (up-to-date)
skipping 'kivy\graphics/cgl_backend\cgl_gl.c' Cython extension (up-to-date)
skipping 'kivy\graphics/cgl_backend\cgl_glew.c' Cython extension (up-to-date)
skipping 'kivy\graphics/cgl_backend\cgl_sdl2.c' Cython extension (up-to-date)
skipping 'kivy\graphics/cgl_backend\cgl_debug.c' Cython extension (up-to-date)
skipping 'kivy\core/text\text_layout.c' Cython extension (up-to-date)
skipping 'kivy\core/window\window_info.c' Cython extension (up-to-date)
skipping 'kivy\graphics\tesselator.c' Cython extension (up-to-date)
skipping 'kivy\graphics\svg.c' Cython extension (up-to-date)
skipping 'kivy\core/window\_window_sdl2.c' Cython extension (up-to-date)
skipping 'kivy\core/image\_img_sdl2.c' Cython extension (up-to-date)
skipping 'kivy\core/text\_text_sdl2.c' Cython extension (up-to-date)
skipping 'kivy\core/audio\audio_sdl2.c' Cython extension (up-to-date)
skipping 'kivy\core/clipboard\_clipboard_sdl2.c' Cython extension (up-to-date)
building 'kivy._event' extension
building 'kivy._clock' extension
building 'kivy.weakproxy' extension
building 'kivy.properties' extension
creating build\temp.win32-3.6
creating build\temp.win32-3.6\Release
creating build\temp.win32-3.6\Release
creating build\temp.win32-3.6\Release
creating build\temp.win32-3.6\Release\kivy
creating build\temp.win32-3.6\Release\kivy
creating build\temp.win32-3.6\Release\kivy
creating build\temp.win32-3.6\Release\kivy
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\_event.c /Fobuild\temp.win32-3.6\Release\kivy\_event.obj
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\_clock.c /Fobuild\temp.win32-3.6\Release\kivy\_clock.obj
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\weakproxy.c /Fobuild\temp.win32-3.6\Release\kivy\weakproxy.obj
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\properties.c /Fobuild\temp.win32-3.6\Release\kivy\properties.obj
_event.c
properties.c
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit__event build\temp.win32-3.6\Release\kivy\_event.obj /OUT:build\lib.win32-3.6\kivy\_event.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\_event.cp36-win32.lib /DEBUG:FULL
_clock.c
weakproxy.c
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_properties build\temp.win32-3.6\Release\kivy\properties.obj /OUT:build\lib.win32-3.6\kivy\properties.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\properties.cp36-win32.lib /DEBUG:FULL
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit__clock build\temp.win32-3.6\Release\kivy\_clock.obj /OUT:build\lib.win32-3.6\kivy\_clock.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\_clock.cp36-win32.lib /DEBUG:FULL
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_weakproxy build\temp.win32-3.6\Release\kivy\weakproxy.obj /OUT:build\lib.win32-3.6\kivy\weakproxy.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\weakproxy.cp36-win32.lib /DEBUG:FULL
   Creating library build\temp.win32-3.6\Release\kivy\_event.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\_event.cp36-win32.exp
Generating code
   Creating library build\temp.win32-3.6\Release\kivy\properties.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\properties.cp36-win32.exp
Generating code
Finished generating code
   Creating library build\temp.win32-3.6\Release\kivy\_clock.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\_clock.cp36-win32.exp
Generating code
   Creating library build\temp.win32-3.6\Release\kivy\weakproxy.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\weakproxy.cp36-win32.exp
Generating code
Finished generating codFinished generating code
e
Finished generating code
building 'kivy.graphics.buffer' extension
creating build\temp.win32-3.6\Release\kivy\graphics
building 'kivy.graphics.context' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics\buffer.c /Fobuild\temp.win32-3.6\Release\kivy\graphics\buffer.obj
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics\context.c /Fobuild\temp.win32-3.6\Release\kivy\graphics\context.obj
building 'kivy.graphics.compiler' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics\compiler.c /Fobuild\temp.win32-3.6\Release\kivy\graphics\compiler.obj
buffer.c
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_buffer build\temp.win32-3.6\Release\kivy\graphics\buffer.obj /OUT:build\lib.win32-3.6\kivy\graphics\buffer.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics\buffer.cp36-win32.lib /DEBUG:FULL
context.c
building 'kivy.graphics.context_instructions' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics\context_instructions.c /Fobuild\temp.win32-3.6\Release\kivy\graphics\context_instructions.obj
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
compiler.c
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_context build\temp.win32-3.6\Release\kivy\graphics\context.obj /OUT:build\lib.win32-3.6\kivy\graphics\context.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics\context.cp36-win32.lib /DEBUG:FULL
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_compiler build\temp.win32-3.6\Release\kivy\graphics\compiler.obj /OUT:build\lib.win32-3.6\kivy\graphics\compiler.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics\compiler.cp36-win32.lib /DEBUG:FULL
   Creating library build\temp.win32-3.6\Release\kivy\graphics\buffer.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics\buffer.cp36-win32.exp
Generating code
Finished generating code
context_instructions.c
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
   Creating library build\temp.win32-3.6\Release\kivy\graphics\context.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics\context.cp36-win32.exp
Generating code
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_context_instructions build\temp.win32-3.6\Release\kivy\graphics\context_instructions.obj /OUT:build\lib.win32-3.6\kivy\graphics\context_instructions.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics\context_instructions.cp36-win32.lib /DEBUG:FULL
   Creating library build\temp.win32-3.6\Release\kivy\graphics\compiler.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics\compiler.cp36-win32.exp
Generating code
Finished generating code
   Creating library build\temp.win32-3.6\Release\kivy\graphics\context_instructions.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics\context_instructions.cp36-win32.exp
Generating code
building 'kivy.graphics.fbo' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics\fbo.c /Fobuild\temp.win32-3.6\Release\kivy\graphics\fbo.obj
Finished generating code
building 'kivy.graphics.gl_instructions' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics\gl_instructions.c /Fobuild\temp.win32-3.6\Release\kivy\graphics\gl_instructions.obj
Finished generating code
fbo.c
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
gl_instructions.c
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_fbo build\temp.win32-3.6\Release\kivy\graphics\fbo.obj /OUT:build\lib.win32-3.6\kivy\graphics\fbo.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics\fbo.cp36-win32.lib /DEBUG:FULL
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
building 'kivy.graphics.instructions' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics\instructions.c /Fobuild\temp.win32-3.6\Release\kivy\graphics\instructions.obj
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_gl_instructions build\temp.win32-3.6\Release\kivy\graphics\gl_instructions.obj /OUT:build\lib.win32-3.6\kivy\graphics\gl_instructions.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics\gl_instructions.cp36-win32.lib /DEBUG:FULL
   Creating library build\temp.win32-3.6\Release\kivy\graphics\fbo.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics\fbo.cp36-win32.exp
Generating code
building 'kivy.graphics.opengl' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics\opengl.c /Fobuild\temp.win32-3.6\Release\kivy\graphics\opengl.obj
Finished generating code
instructions.c
   Creating library build\temp.win32-3.6\Release\kivy\graphics\gl_instructions.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics\gl_instructions.cp36-win32.exp
Generating code
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
Finished generating code
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_instructions build\temp.win32-3.6\Release\kivy\graphics\instructions.obj /OUT:build\lib.win32-3.6\kivy\graphics\instructions.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics\instructions.cp36-win32.lib /DEBUG:FULL
opengl.c
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_opengl build\temp.win32-3.6\Release\kivy\graphics\opengl.obj /OUT:build\lib.win32-3.6\kivy\graphics\opengl.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics\opengl.cp36-win32.lib /DEBUG:FULL
   Creating library build\temp.win32-3.6\Release\kivy\graphics\instructions.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics\instructions.cp36-win32.exp
Generating code
building 'kivy.graphics.opengl_utils' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics\opengl_utils.c /Fobuild\temp.win32-3.6\Release\kivy\graphics\opengl_utils.obj
Finished generating code
building 'kivy.graphics.shader' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics\shader.c /Fobuild\temp.win32-3.6\Release\kivy\graphics\shader.obj
   Creating library build\temp.win32-3.6\Release\kivy\graphics\opengl.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics\opengl.cp36-win32.exp
Generating code
opengl_utils.c
shader.c
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_opengl_utils build\temp.win32-3.6\Release\kivy\graphics\opengl_utils.obj /OUT:build\lib.win32-3.6\kivy\graphics\opengl_utils.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics\opengl_utils.cp36-win32.lib /DEBUG:FULL
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_shader build\temp.win32-3.6\Release\kivy\graphics\shader.obj /OUT:build\lib.win32-3.6\kivy\graphics\shader.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics\shader.cp36-win32.lib /DEBUG:FULL
building 'kivy.graphics.stencil_instructions' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics\stencil_instructions.c /Fobuild\temp.win32-3.6\Release\kivy\graphics\stencil_instructions.obj
   Creating library build\temp.win32-3.6\Release\kivy\graphics\opengl_utils.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics\opengl_utils.cp36-win32.exp
Generating code
Finished generating code
   Creating library build\temp.win32-3.6\Release\kivy\graphics\shader.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics\shader.cp36-win32.exp
Generating code
stencil_instructions.c
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_stencil_instructions build\temp.win32-3.6\Release\kivy\graphics\stencil_instructions.obj /OUT:build\lib.win32-3.6\kivy\graphics\stencil_instructions.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics\stencil_instructions.cp36-win32.lib /DEBUG:FULL
building 'kivy.graphics.scissor_instructions' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics\scissor_instructions.c /Fobuild\temp.win32-3.6\Release\kivy\graphics\scissor_instructions.obj
   Creating library build\temp.win32-3.6\Release\kivy\graphics\stencil_instructions.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics\stencil_instructions.cp36-win32.exp
Generating code
Finished generating code
scissor_instructions.c
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_scissor_instructions build\temp.win32-3.6\Release\kivy\graphics\scissor_instructions.obj /OUT:build\lib.win32-3.6\kivy\graphics\scissor_instructions.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics\scissor_instructions.cp36-win32.lib /DEBUG:FULL
building 'kivy.graphics.texture' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics\texture.c /Fobuild\temp.win32-3.6\Release\kivy\graphics\texture.obj
   Creating library build\temp.win32-3.6\Release\kivy\graphics\scissor_instructions.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics\scissor_instructions.cp36-win32.exp
Generating code
Finished generating code
texture.c
Finished generating code
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
building 'kivy.graphics.transformation' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics\transformation.c /Fobuild\temp.win32-3.6\Release\kivy\graphics\transformation.obj
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_texture build\temp.win32-3.6\Release\kivy\graphics\texture.obj /OUT:build\lib.win32-3.6\kivy\graphics\texture.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics\texture.cp36-win32.lib /DEBUG:FULL
building 'kivy.graphics.vbo' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics\vbo.c /Fobuild\temp.win32-3.6\Release\kivy\graphics\vbo.obj
transformation.c
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_transformation build\temp.win32-3.6\Release\kivy\graphics\transformation.obj /OUT:build\lib.win32-3.6\kivy\graphics\transformation.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics\transformation.cp36-win32.lib /DEBUG:FULL
   Creating library build\temp.win32-3.6\Release\kivy\graphics\texture.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics\texture.cp36-win32.exp
Generating code
vbo.c
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
 kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
CD:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'r
eating library build\temp.win32-3.6\Release\kivy\graphics\transformation.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics\transformatiC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_vbo build\temp.win32-3.6\Release\kivy\graphics\vbo.obj /OUT:build\lib.win32-3.6\kivy\graphics\vbo.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics\vbo.cp36-win32.lib /DEBUG:FULL
on.cp36-win32.exp
Generating code
   Creating library build\temp.win32-3.6\Release\kivy\graphics\vbo.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics\vbo.cp36-win32.exp
Generating code
Finished generating code
Finished generating code
Finished generating code
building 'kivy.graphics.vertex' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics\vertex.c /Fobuild\temp.win32-3.6\Release\kivy\graphics\vertex.obj
building 'kivy.graphics.vertex_instructions' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics\vertex_instructions.c /Fobuild\temp.win32-3.6\Release\kivy\graphics\vertex_instructions.obj
vertex.c
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_vertex build\temp.win32-3.6\Release\kivy\graphics\vertex.obj /OUT:build\lib.win32-3.6\kivy\graphics\vertex.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics\vertex.cp36-win32.lib /DEBUG:FULL
vertex_instructions.c
Finished generating code
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
building 'kivy.graphics.cgl' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics\cgl.c /Fobuild\temp.win32-3.6\Release\kivy\graphics\cgl.obj
   Creating library build\temp.win32-3.6\Release\kivy\graphics\vertex.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics\vertex.cp36-win32.exp
Generating code
Finished generating code
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_vertex_instructions build\temp.win32-3.6\Release\kivy\graphics\vertex_instructions.obj /OUT:build\lib.win32-3.6\kivy\graphics\vertex_instructions.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics\vertex_instructions.cp36-win32.lib /DEBUG:FULL
cgl.c
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_cgl build\temp.win32-3.6\Release\kivy\graphics\cgl.obj /OUT:build\lib.win32-3.6\kivy\graphics\cgl.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics\cgl.cp36-win32.lib /DEBUG:FULL
   Creating library build\temp.win32-3.6\Release\kivy\graphics\vertex_instructions.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics\vertex_instructions.cp36-win32.exp
Generating code
building 'kivy.graphics.cgl_backend.cgl_mock' extension
creating build\temp.win32-3.6\Release\kivy\graphics\cgl_backend
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics/cgl_backend\cgl_mock.c /Fobuild\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_mock.obj
   Creating library build\temp.win32-3.6\Release\kibuilding 'kivy.graphics.cgl_backend.cgl_gl' extension
vC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics/cgl_backend\cgl_gl.c /Fobuild\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_gl.obj
y\graphics\cgl.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphiccgl_mock.c
s\cgl.cp36-win32.exp
Generating code
Finished generating code
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_cgl_mock build\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_mock.obj /OUT:build\lib.win32-3.6\kivy\graphics\cgl_backend\cgl_mock.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_mock.cp36-win32.lib /DEBUG:FULL
cgl_gl.c
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" opengl32.lib glew32.lib /EXPORT:PyInit_cgl_gl build\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_gl.obj /OUT:build\lib.win32-3.6\kivy\graphics\cgl_backend\cgl_gl.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_gl.cp36-win32.lib /DEBUG:FULL
   Creating library build\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_mock.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_mock.cp36-win32.exp
Generating code
Finished generating code
building 'kivy.graphics.cgl_backend.cgl_glew' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics/cgl_backend\cgl_glew.c /Fobuild\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_glew.obj
   Creating library build\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_gl.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_gl.cp36-win32.exp
Generating code
Finished generating code
cgl_glew.c
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" opengl32.lib glew32.lib /EXPORT:PyInit_cgl_glew build\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_glew.obj /OUT:build\lib.win32-3.6\kivy\graphics\cgl_backend\cgl_glew.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_glew.cp36-win32.lib /DEBUG:FULL
building 'kivy.graphics.cgl_backend.cgl_sdl2' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include\SDL2 -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include\SDL2 -I/usr/local/include/SDL2 -I/usr/include/SDL2 -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics/cgl_backend\cgl_sdl2.c /Fobuild\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_sdl2.obj
building 'kivy.graphics.cgl_backend.cgl_debug' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics/cgl_backend\cgl_debug.c /Fobuild\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_debug.obj
   Creating library build\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_glew.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_glew.cp36-win32.exp
Generating code
Finished generating code
cgl_sdl2.c
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
cgl_debug.c
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include\SDL2 /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\include\SDL2 /LIBPATH:/usr/local/include/SDL2 /LIBPATH:/usr/include/SDL2 /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" SDL2.lib SDL2_ttf.lib SDL2_image.lib SDL2_mixer.lib /EXPORT:PyInit_cgl_sdl2 build\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_sdl2.obj /OUT:build\lib.win32-3.6\kivy\graphics\cgl_backend\cgl_sdl2.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_sdl2.cp36-win32.lib /DEBUG:FULL
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
Finished generating code
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_cgl_debug build\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_debug.obj /OUT:build\lib.win32-3.6\kivy\graphics\cgl_backend\cgl_debug.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_debug.cp36-win32.lib /DEBUG:FULL
   Creating library build\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_sdl2.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_sdl2.cp36-win32.exp
Generating code
Finished generating code
building 'kivy.core.text.text_layout' extension
creating build\temp.win32-3.6\Release\kivy\core
creating build\temp.win32-3.6\Release\kivy\core\text
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\core/text\text_layout.c /Fobuild\temp.win32-3.6\Release\kivy\core/text\text_layout.obj
   Creating library build\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_debug.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics/cgl_backend\cgl_debug.cp36-win32.exp
Generating code
building 'kivy.core.window.window_info' extension
creating build\temp.win32-3.6\Release\kivy\core\window
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\core/window\window_info.c /Fobuild\temp.win32-3.6\Release\kivy\core/window\window_info.obj
text_layout.c
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_text_layout build\temp.win32-3.6\Release\kivy\core/text\text_layout.obj /OUT:build\lib.win32-3.6\kivy\core\text\text_layout.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\core/text\text_layout.cp36-win32.lib /DEBUG:FULL
Finished generating code
building 'kivy.graphics.tesselator' extension
creating build\temp.win32-3.6\Release\kivy\lib
creating build\temp.win32-3.6\Release\kivy\lib\libtess2
creating build\temp.win32-3.6\Release\kivy\lib\libtess2\Source
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy/lib/libtess2/Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics\tesselator.c /Fobuild\temp.win32-3.6\Release\kivy\graphics\tesselator.obj
window_info.c
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_window_info build\temp.win32-3.6\Release\kivy\core/window\window_info.obj /OUT:build\lib.win32-3.6\kivy\core\window\window_info.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\core/window\window_info.cp36-win32.lib /DEBUG:FULL
   Creating library build\temp.win32-3.6\Release\kivy\core/text\text_layout.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\core/text\text_layout.cp36-win32.exp
Generating code
tesselator.c
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy/lib/libtess2/Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\lib/libtess2/Source/bucketalloc.c /Fobuild\temp.win32-3.6\Release\kivy\lib/libtess2/Source/bucketalloc.obj
   Creating library build\temp.win32-3.6\Release\kivy\core/window\window_info.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\core/window\window_info.cp36-win32.exp
Generating code
Finished generating code
Finished generating code
building 'kivy.graphics.svg' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\graphics\svg.c /Fobuild\temp.win32-3.6\Release\kivy\graphics\svg.obj
bucketalloc.c
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy/lib/libtess2/Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\lib/libtess2/Source/dict.c /Fobuild\temp.win32-3.6\Release\kivy\lib/libtess2/Source/dict.obj
svg.c
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
dict.c
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy/lib/libtess2/Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\lib/libtess2/Source/geom.c /Fobuild\temp.win32-3.6\Release\kivy\lib/libtess2/Source/geom.obj
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_svg build\temp.win32-3.6\Release\kivy\graphics\svg.obj /OUT:build\lib.win32-3.6\kivy\graphics\svg.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics\svg.cp36-win32.lib /DEBUG:FULL
building 'kivy.core.window._window_sdl2' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include\SDL2 -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include\SDL2 -I/usr/local/include/SDL2 -I/usr/include/SDL2 -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\core/window\_window_sdl2.c /Fobuild\temp.win32-3.6\Release\kivy\core/window\_window_sdl2.obj
building 'kivy.core.image._img_sdl2' extension
creating build\temp.win32-3.6\Release\kivy\core\image
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include\SDL2 -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include\SDL2 -I/usr/local/include/SDL2 -I/usr/include/SDL2 -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\core/image\_img_sdl2.c /Fobuild\temp.win32-3.6\Release\kivy\core/image\_img_sdl2.obj
geom.c
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy/lib/libtess2/Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\lib/libtess2/Source/mesh.c /Fobuild\temp.win32-3.6\Release\kivy\lib/libtess2/Source/mesh.obj
   Creating library build\temp.win32-3.6\Release\kivy\graphics\svg.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics\svg.cp36-win32.exp
Generating code
_window_sdl2.c
kivy\include\gl_redirect.h(44): warning C4005: 'GL_EXT_disjoint_timer_query': macro redefinition
_img_sdl2.c
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(10276): note: see previous definition of 'GL_EXT_disjoint_timer_query'
kivy\include\gl_redirect.h(51): warning C4005: 'GL_EXT_texture_border_clamp': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12546): note: see previous definition of 'GL_EXT_texture_border_clamp'
kivy\include\gl_redirect.h(52): warning C4005: 'GL_EXT_texture_buffer': macro redefinition
D:\tools\tools\python366-32with-pdb\include\GL/glew.h(12568): note: see previous definition of 'GL_EXT_texture_buffer'
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include\SDL2 /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\include\SDL2 /LIBPATH:/usr/local/include/SDL2 /LIBPATH:/usr/include/SDL2 /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" SDL2.lib SDL2_ttf.lib SDL2_image.lib SDL2_mixer.lib /EXPORT:PyInit__window_sdl2 build\temp.win32-3.6\Release\kivy\core/window\_window_sdl2.obj /OUT:build\lib.win32-3.6\kivy\core\window\_window_sdl2.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\core/window\_window_sdl2.cp36-win32.lib /DEBUG:FULL
mesh.c
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy/lib/libtess2/Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\lib/libtess2/Source/priorityq.c /Fobuild\temp.win32-3.6\Release\kivy\lib/libtess2/Source/priorityq.obj
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include\SDL2 /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\include\SDL2 /LIBPATH:/usr/local/include/SDL2 /LIBPATH:/usr/include/SDL2 /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" SDL2.lib SDL2_ttf.lib SDL2_image.lib SDL2_mixer.lib /EXPORT:PyInit__img_sdl2 build\temp.win32-3.6\Release\kivy\core/image\_img_sdl2.obj /OUT:build\lib.win32-3.6\kivy\core\image\_img_sdl2.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\core/image\_img_sdl2.cp36-win32.lib /DEBUG:FULL
   Creating library build\temp.win32-3.6\Release\kivy\core/window\_window_sdl2.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\core/window\_window_sdl2.cp36-win32.exp
Generating code
Finished generating code
priorityq.c
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy/lib/libtess2/Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\lib/libtess2/Source/sweep.c /Fobuild\temp.win32-3.6\Release\kivy\lib/libtess2/Source/sweep.obj
   Creating library build\temp.win32-3.6\Release\kivy\core/image\_img_sdl2.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\core/image\_img_sdl2.cp36-win32.exp
Generating code
Finished generating code
sweep.c
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -Ikivy/lib/libtess2/Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\lib/libtess2/Source/tess.c /Fobuild\temp.win32-3.6\Release\kivy\lib/libtess2/Source/tess.obj
building 'kivy.core.text._text_sdl2' extension
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include\SDL2 -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include\SDL2 -I/usr/local/include/SDL2 -I/usr/include/SDL2 -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\core/text\_text_sdl2.c /Fobuild\temp.win32-3.6\Release\kivy\core/text\_text_sdl2.obj
tess.c
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" /EXPORT:PyInit_tesselator build\temp.win32-3.6\Release\kivy\graphics\tesselator.obj build\temp.win32-3.6\Release\kivy\lib/libtess2/Source/bucketalloc.obj build\temp.win32-3.6\Release\kivy\lib/libtess2/Source/dict.obj build\temp.win32-3.6\Release\kivy\lib/libtess2/Source/geom.obj build\temp.win32-3.6\Release\kivy\lib/libtess2/Source/mesh.obj build\temp.win32-3.6\Release\kivy\lib/libtess2/Source/priorityq.obj build\temp.win32-3.6\Release\kivy\lib/libtess2/Source/sweep.obj build\temp.win32-3.6\Release\kivy\lib/libtess2/Source/tess.obj /OUT:build\lib.win32-3
.6\kivy\graphics\tesselator.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\graphics\tesselator.cp36-win32.lib /DEBUG:FULL
building 'kivy.core.audio.audio_sdl2' extension
creating build\temp.win32-3.6\Release\kivy\core\audio
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include\SDL2 -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include\SDL2 -I/usr/local/include/SDL2 -I/usr/include/SDL2 -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\core/audio\audio_sdl2.c /Fobuild\temp.win32-3.6\Release\kivy\core/audio\audio_sdl2.obj
_text_sdl2.c
Finished generating code
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include\SDL2 /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\include\SDL2 /LIBPATH:/usr/local/include/SDL2 /LIBPATH:/usr/include/SDL2 /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" SDL2.lib SDL2_ttf.lib SDL2_image.lib SDL2_mixer.lib /EXPORT:PyInit__text_sdl2 build\temp.win32-3.6\Release\kivy\core/text\_text_sdl2.obj /OUT:build\lib.win32-3.6\kivy\core\text\_text_sdl2.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\core/text\_text_sdl2.cp36-win32.lib /DEBUG:FULL
   Creating library build\temp.win32-3.6\Release\kivy\graphics\tesselator.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\graphics\tesselator.cp36-win32.exp
Generating code
audio_sdl2.c
Finished generating code
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include\SDL2 /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\include\SDL2 /LIBPATH:/usr/local/include/SDL2 /LIBPATH:/usr/include/SDL2 /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" SDL2.lib SDL2_ttf.lib SDL2_image.lib SDL2_mixer.lib /EXPORT:PyInit_audio_sdl2 build\temp.win32-3.6\Release\kivy\core/audio\audio_sdl2.obj /OUT:build\lib.win32-3.6\kivy\core\audio\audio_sdl2.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\core/audio\audio_sdl2.cp36-win32.lib /DEBUG:FULL
   Creating library build\temp.win32-3.6\Release\kivy\core/text\_text_sdl2.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\core/text\_text_sdl2.cp36-win32.exp
Generating code
Finished generating code
building 'kivy.core.clipboard._clipboard_sdl2' extension
creating build\temp.win32-3.6\Release\kivy\core\clipboard
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -Ikivy\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include\SDL2 -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include\SDL2 -I/usr/local/include/SDL2 -I/usr/include/SDL2 -IC:\Users\guanglin.liang\pythonEnv\withPdbInfo\include -ID:\tools\tools\python366-32with-pdb\include -ID:\tools\tools\python366-32with-pdb\include "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE" "-IC:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt" "-IC:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\include\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\shared" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\um" "-IC:\Program Files (x86)\Windows Kits\8.1\include\\winrt" /Tckivy\core/clipboard\_clipboard_sdl2.c /Fobuild\temp.win32-3.6\Release\kivy\core/clipboard\_clipboard_sdl2.obj
   Creating library build\temp.win32-3.6\Release\kivy\core/audio\audio_sdl2.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\core/audio\audio_sdl2.cp36-win32.exp
Generating code
Finished generating code
_clipboard_sdl2.c
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include\SDL2 /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\include\SDL2 /LIBPATH:/usr/local/include/SDL2 /LIBPATH:/usr/include/SDL2 /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\libs /LIBPATH:D:\tools\tools\python366-32with-pdb\libs /LIBPATH:D:\tools\tools\python366-32with-pdb /LIBPATH:C:\Users\guanglin.liang\pythonEnv\withPdbInfo\PCbuild\win32 "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB" "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.10240.0\ucrt\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\NETFXSDK\4.6\lib\um\x86" "/LIBPATH:C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86" SDL2.lib SDL2_ttf.lib SDL2_image.lib SDL2_mixer.lib /EXPORT:PyInit__clipboard_sdl2 build\temp.win32-3.6\Release\kivy\core/clipboard\_clipboard_sdl2.obj /OUT:build\lib.win32-3.6\kivy\core\clipboard\_clipboard_sdl2.cp36-win32.pyd /IMPLIB:build\temp.win32-3.6\Release\kivy\core/clipboard\_clipboard_sdl2.cp36-win32.lib /DEBUG:FULL
   Creating library build\temp.win32-3.6\Release\kivy\core/clipboard\_clipboard_sdl2.cp36-win32.lib and object build\temp.win32-3.6\Release\kivy\core/clipboard\_clipboard_sdl2.cp36-win32.exp
Generating code
Finished generating code

(withPdbInfo) D:\workspace\Kivy-2.0.0>set user_sdl2=1

(withPdbInfo) D:\workspace\Kivy-2.0.0>python setup.py bdist_wheel
sdl2 path:['C:\\Users\\guanglin.liang\\pythonEnv\\withPdbInfo\\share\\sdl2\\bin']
[INFO   ] [Logger      ] Record log in C:\Users\guanglin.liang\.kivy\logs\kivy_22-06-02_3.txt
[INFO   ] [deps        ] Successfully imported "kivy_deps.angle" 0.3.0
[INFO   ] [deps        ] Successfully imported "kivy_deps.glew" 0.3.0
[INFO   ] [deps        ] Successfully imported "kivy_deps.sdl2" 0.3.1
[INFO   ] [deps        ] Successfully imported "kivy_deps.sdl2_dev" 0.4.3
[INFO   ] [Kivy        ] v2.0.0
[INFO   ] [Kivy        ] Installed at "D:\workspace\Kivy-2.0.0\kivy\__init__.py"
[INFO   ] [Python      ] v3.6.6 (v3.6.6:4cf1f54eb7, Jun 27 2018, 02:47:15) [MSC v.1900 32 bit (Intel)]
[INFO   ] [Python      ] Interpreter at "C:\Users\guanglin.liang\pythonEnv\withPdbInfo\Scripts\python.exe"
Current directory is: D:\workspace\Kivy-2.0.0
Source and initial build directory is:
Python path is:
D:\workspace\Kivy-2.0.0
C:\Users\guanglin.liang\pythonEnv\withPdbInfo\Scripts\python36.zip
D:\tools\tools\python366-32with-pdb\DLLs
D:\tools\tools\python366-32with-pdb\lib
D:\tools\tools\python366-32with-pdb
C:\Users\guanglin.liang\pythonEnv\withPdbInfo
C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages
C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages\pypiwin32-223-py3.6.egg
C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages\pygments-2.12.0-py3.6.egg
C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages\docutils-0.18.1-py3.6.egg
C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages\cpython_example-0.0.1-py3.6-win32.egg
C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages\win32
C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages\win32\lib
C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages\Pythonwin
D:\workspace\Kivy-2.0.0\kivy\modules
C:\Users\guanglin.liang\.kivy\mods


Found Cython at C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages\Cython\__init__.py
Detected supported Cython version 0.29.19
User distribution detected, avoid portable command.
Using this graphics system: OpenGL
WARNING: A problem occurred while running pkg-config --libs --cflags gstreamer-1.0 (code 1)

b"'pkg-config' \xb2\xbb\xca\xc7\xc4\xda\xb2\xbf\xbb\xf2\xcd\xe2\xb2\xbf\xc3\xfc\xc1\xee\xa3\xac\xd2\xb2\xb2\xbb\xca\xc7\xbf\xc9\xd4\xcb\xd0\xd0\xb5\xc4\xb3\xcc\xd0\xf2\r\n\xbb\xf2\xc5\xfa\xb4\xa6\xc0\xed\xce\xc4\xbc\xfe\xa1\xa3\r\n"

WARNING: A problem occurred while running pkg-config --libs --cflags gstreamer-1.0 (code 1)

b"'pkg-config' \xb2\xbb\xca\xc7\xc4\xda\xb2\xbf\xbb\xf2\xcd\xe2\xb2\xbf\xc3\xfc\xc1\xee\xa3\xac\xd2\xb2\xb2\xbb\xca\xc7\xbf\xc9\xd4\xcb\xd0\xd0\xb5\xc4\xb3\xcc\xd0\xf2\r\n\xbb\xf2\xc5\xfa\xb4\xa6\xc0\xed\xce\xc4\xbc\xfe\xa1\xa3\r\n"

WARNING: A problem occurred while running pkg-config --libs --cflags sdl2 SDL2_ttf SDL2_image SDL2_mixer (code 1)

b"'pkg-config' \xb2\xbb\xca\xc7\xc4\xda\xb2\xbf\xbb\xf2\xcd\xe2\xb2\xbf\xc3\xfc\xc1\xee\xa3\xac\xd2\xb2\xb2\xbb\xca\xc7\xbf\xc9\xd4\xcb\xd0\xd0\xb5\xc4\xb3\xcc\xd0\xf2\r\n\xbb\xf2\xc5\xfa\xb4\xa6\xc0\xed\xce\xc4\xbc\xfe\xa1\xa3\r\n"

SDL2: found SDL header at C:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include\SDL2\SDL.h
SDL2: found SDL_mixer header at C:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include\SDL2\SDL_mixer.h
SDL2: found SDL_ttf header at C:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include\SDL2\SDL_ttf.h
SDL2: found SDL_image header at C:\Users\guanglin.liang\pythonEnv\withPdbInfo\Include\SDL2\SDL_image.h
running bdist_wheel
running build
running build_py
running build_ext
Building extensions in parallel using 4 cores
Updated build directory to: build\lib.win32-3.6
Build configuration is:
 * use_rpi = 0
 * use_egl = 0
 * use_opengl_es2 = 0
 * use_opengl_mock = 0
 * use_sdl2 = 1
 * use_pangoft2 = 0
 * use_ios = 0
 * use_android = 0
 * use_mesagl = 0
 * use_x11 = 0
 * use_wayland = 0
 * use_gstreamer = 0
 * use_avfoundation = 0
 * use_osx_frameworks = 0
 * debug_gl = 0
 * kivy_sdl_gl_alpha_size = 8
 * debug = False
Detected compiler is msvc
skipping 'kivy\_event.c' Cython extension (up-to-date)
skipping 'kivy\_clock.c' Cython extension (up-to-date)
skipping 'kivy\weakproxy.c' Cython extension (up-to-date)
skipping 'kivy\properties.c' Cython extension (up-to-date)
skipping 'kivy\graphics\buffer.c' Cython extension (up-to-date)
skipping 'kivy\graphics\context.c' Cython extension (up-to-date)
skipping 'kivy\graphics\compiler.c' Cython extension (up-to-date)
skipping 'kivy\graphics\context_instructions.c' Cython extension (up-to-date)
skipping 'kivy\graphics\fbo.c' Cython extension (up-to-date)
skipping 'kivy\graphics\gl_instructions.c' Cython extension (up-to-date)
skipping 'kivy\graphics\instructions.c' Cython extension (up-to-date)
skipping 'kivy\graphics\opengl.c' Cython extension (up-to-date)
skipping 'kivy\graphics\opengl_utils.c' Cython extension (up-to-date)
skipping 'kivy\graphics\shader.c' Cython extension (up-to-date)
skipping 'kivy\graphics\stencil_instructions.c' Cython extension (up-to-date)
skipping 'kivy\graphics\scissor_instructions.c' Cython extension (up-to-date)
skipping 'kivy\graphics\texture.c' Cython extension (up-to-date)
skipping 'kivy\graphics\transformation.c' Cython extension (up-to-date)
skipping 'kivy\graphics\vbo.c' Cython extension (up-to-date)
skipping 'kivy\graphics\vertex.c' Cython extension (up-to-date)
skipping 'kivy\graphics\vertex_instructions.c' Cython extension (up-to-date)
skipping 'kivy\graphics\cgl.c' Cython extension (up-to-date)
skipping 'kivy\graphics/cgl_backend\cgl_mock.c' Cython extension (up-to-date)
skipping 'kivy\graphics/cgl_backend\cgl_gl.c' Cython extension (up-to-date)
skipping 'kivy\graphics/cgl_backend\cgl_glew.c' Cython extension (up-to-date)
skipping 'kivy\graphics/cgl_backend\cgl_sdl2.c' Cython extension (up-to-date)
skipping 'kivy\graphics/cgl_backend\cgl_debug.c' Cython extension (up-to-date)
skipping 'kivy\core/text\text_layout.c' Cython extension (up-to-date)
skipping 'kivy\core/window\window_info.c' Cython extension (up-to-date)
skipping 'kivy\graphics\tesselator.c' Cython extension (up-to-date)
skipping 'kivy\graphics\svg.c' Cython extension (up-to-date)
skipping 'kivy\core/window\_window_sdl2.c' Cython extension (up-to-date)
skipping 'kivy\core/image\_img_sdl2.c' Cython extension (up-to-date)
skipping 'kivy\core/text\_text_sdl2.c' Cython extension (up-to-date)
skipping 'kivy\core/audio\audio_sdl2.c' Cython extension (up-to-date)
skipping 'kivy\core/clipboard\_clipboard_sdl2.c' Cython extension (up-to-date)
installing to build\bdist.win32\wheel
running install
running install_lib
creating build\bdist.win32
creating build\bdist.win32\wheel
creating build\bdist.win32\wheel\kivy
copying build\lib.win32-3.6\kivy\animation.py -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\app.py -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\atlas.py -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\base.py -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\cache.py -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\clock.py -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\compat.py -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\config.py -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\context.py -> build\bdist.win32\wheel\.\kivy
creating build\bdist.win32\wheel\kivy\core
creating build\bdist.win32\wheel\kivy\core\audio
copying build\lib.win32-3.6\kivy\core\audio\audio_android.py -> build\bdist.win32\wheel\.\kivy\core\audio
copying build\lib.win32-3.6\kivy\core\audio\audio_avplayer.py -> build\bdist.win32\wheel\.\kivy\core\audio
copying build\lib.win32-3.6\kivy\core\audio\audio_ffpyplayer.py -> build\bdist.win32\wheel\.\kivy\core\audio
copying build\lib.win32-3.6\kivy\core\audio\audio_gstplayer.py -> build\bdist.win32\wheel\.\kivy\core\audio
copying build\lib.win32-3.6\kivy\core\audio\audio_pygame.py -> build\bdist.win32\wheel\.\kivy\core\audio
copying build\lib.win32-3.6\kivy\core\audio\audio_sdl2.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\core\audio
copying build\lib.win32-3.6\kivy\core\audio\audio_sdl2.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\core\audio
copying build\lib.win32-3.6\kivy\core\audio\__init__.py -> build\bdist.win32\wheel\.\kivy\core\audio
creating build\bdist.win32\wheel\kivy\core\camera
copying build\lib.win32-3.6\kivy\core\camera\camera_android.py -> build\bdist.win32\wheel\.\kivy\core\camera
copying build\lib.win32-3.6\kivy\core\camera\camera_gi.py -> build\bdist.win32\wheel\.\kivy\core\camera
copying build\lib.win32-3.6\kivy\core\camera\camera_opencv.py -> build\bdist.win32\wheel\.\kivy\core\camera
copying build\lib.win32-3.6\kivy\core\camera\camera_picamera.py -> build\bdist.win32\wheel\.\kivy\core\camera
copying build\lib.win32-3.6\kivy\core\camera\__init__.py -> build\bdist.win32\wheel\.\kivy\core\camera
creating build\bdist.win32\wheel\kivy\core\clipboard
copying build\lib.win32-3.6\kivy\core\clipboard\clipboard_android.py -> build\bdist.win32\wheel\.\kivy\core\clipboard
copying build\lib.win32-3.6\kivy\core\clipboard\clipboard_dbusklipper.py -> build\bdist.win32\wheel\.\kivy\core\clipboard
copying build\lib.win32-3.6\kivy\core\clipboard\clipboard_dummy.py -> build\bdist.win32\wheel\.\kivy\core\clipboard
copying build\lib.win32-3.6\kivy\core\clipboard\clipboard_gtk3.py -> build\bdist.win32\wheel\.\kivy\core\clipboard
copying build\lib.win32-3.6\kivy\core\clipboard\clipboard_nspaste.py -> build\bdist.win32\wheel\.\kivy\core\clipboard
copying build\lib.win32-3.6\kivy\core\clipboard\clipboard_pygame.py -> build\bdist.win32\wheel\.\kivy\core\clipboard
copying build\lib.win32-3.6\kivy\core\clipboard\clipboard_sdl2.py -> build\bdist.win32\wheel\.\kivy\core\clipboard
copying build\lib.win32-3.6\kivy\core\clipboard\clipboard_winctypes.py -> build\bdist.win32\wheel\.\kivy\core\clipboard
copying build\lib.win32-3.6\kivy\core\clipboard\clipboard_xclip.py -> build\bdist.win32\wheel\.\kivy\core\clipboard
copying build\lib.win32-3.6\kivy\core\clipboard\clipboard_xsel.py -> build\bdist.win32\wheel\.\kivy\core\clipboard
copying build\lib.win32-3.6\kivy\core\clipboard\_clipboard_ext.py -> build\bdist.win32\wheel\.\kivy\core\clipboard
copying build\lib.win32-3.6\kivy\core\clipboard\_clipboard_sdl2.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\core\clipboard
copying build\lib.win32-3.6\kivy\core\clipboard\_clipboard_sdl2.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\core\clipboard
copying build\lib.win32-3.6\kivy\core\clipboard\__init__.py -> build\bdist.win32\wheel\.\kivy\core\clipboard
creating build\bdist.win32\wheel\kivy\core\gl
copying build\lib.win32-3.6\kivy\core\gl\__init__.py -> build\bdist.win32\wheel\.\kivy\core\gl
creating build\bdist.win32\wheel\kivy\core\image
copying build\lib.win32-3.6\kivy\core\image\img_dds.py -> build\bdist.win32\wheel\.\kivy\core\image
copying build\lib.win32-3.6\kivy\core\image\img_ffpyplayer.py -> build\bdist.win32\wheel\.\kivy\core\image
copying build\lib.win32-3.6\kivy\core\image\img_pil.py -> build\bdist.win32\wheel\.\kivy\core\image
copying build\lib.win32-3.6\kivy\core\image\img_pygame.py -> build\bdist.win32\wheel\.\kivy\core\image
copying build\lib.win32-3.6\kivy\core\image\img_sdl2.py -> build\bdist.win32\wheel\.\kivy\core\image
copying build\lib.win32-3.6\kivy\core\image\img_tex.py -> build\bdist.win32\wheel\.\kivy\core\image
copying build\lib.win32-3.6\kivy\core\image\_img_sdl2.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\core\image
copying build\lib.win32-3.6\kivy\core\image\_img_sdl2.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\core\image
copying build\lib.win32-3.6\kivy\core\image\__init__.py -> build\bdist.win32\wheel\.\kivy\core\image
creating build\bdist.win32\wheel\kivy\core\spelling
copying build\lib.win32-3.6\kivy\core\spelling\spelling_enchant.py -> build\bdist.win32\wheel\.\kivy\core\spelling
copying build\lib.win32-3.6\kivy\core\spelling\spelling_osxappkit.py -> build\bdist.win32\wheel\.\kivy\core\spelling
copying build\lib.win32-3.6\kivy\core\spelling\__init__.py -> build\bdist.win32\wheel\.\kivy\core\spelling
creating build\bdist.win32\wheel\kivy\core\text
copying build\lib.win32-3.6\kivy\core\text\markup.py -> build\bdist.win32\wheel\.\kivy\core\text
copying build\lib.win32-3.6\kivy\core\text\text_layout.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\core\text
copying build\lib.win32-3.6\kivy\core\text\text_layout.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\core\text
copying build\lib.win32-3.6\kivy\core\text\text_layout.pxd -> build\bdist.win32\wheel\.\kivy\core\text
copying build\lib.win32-3.6\kivy\core\text\text_pango.py -> build\bdist.win32\wheel\.\kivy\core\text
copying build\lib.win32-3.6\kivy\core\text\text_pil.py -> build\bdist.win32\wheel\.\kivy\core\text
copying build\lib.win32-3.6\kivy\core\text\text_pygame.py -> build\bdist.win32\wheel\.\kivy\core\text
copying build\lib.win32-3.6\kivy\core\text\text_sdl2.py -> build\bdist.win32\wheel\.\kivy\core\text
copying build\lib.win32-3.6\kivy\core\text\_text_sdl2.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\core\text
copying build\lib.win32-3.6\kivy\core\text\_text_sdl2.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\core\text
copying build\lib.win32-3.6\kivy\core\text\__init__.py -> build\bdist.win32\wheel\.\kivy\core\text
creating build\bdist.win32\wheel\kivy\core\video
copying build\lib.win32-3.6\kivy\core\video\video_ffmpeg.py -> build\bdist.win32\wheel\.\kivy\core\video
copying build\lib.win32-3.6\kivy\core\video\video_ffpyplayer.py -> build\bdist.win32\wheel\.\kivy\core\video
copying build\lib.win32-3.6\kivy\core\video\video_gstplayer.py -> build\bdist.win32\wheel\.\kivy\core\video
copying build\lib.win32-3.6\kivy\core\video\video_null.py -> build\bdist.win32\wheel\.\kivy\core\video
copying build\lib.win32-3.6\kivy\core\video\__init__.py -> build\bdist.win32\wheel\.\kivy\core\video
creating build\bdist.win32\wheel\kivy\core\window
copying build\lib.win32-3.6\kivy\core\window\window_attrs.pxi -> build\bdist.win32\wheel\.\kivy\core\window
copying build\lib.win32-3.6\kivy\core\window\window_egl_rpi.py -> build\bdist.win32\wheel\.\kivy\core\window
copying build\lib.win32-3.6\kivy\core\window\window_info.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\core\window
copying build\lib.win32-3.6\kivy\core\window\window_info.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\core\window
copying build\lib.win32-3.6\kivy\core\window\window_info.pxd -> build\bdist.win32\wheel\.\kivy\core\window
copying build\lib.win32-3.6\kivy\core\window\window_pygame.py -> build\bdist.win32\wheel\.\kivy\core\window
copying build\lib.win32-3.6\kivy\core\window\window_sdl2.py -> build\bdist.win32\wheel\.\kivy\core\window
copying build\lib.win32-3.6\kivy\core\window\_window_sdl2.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\core\window
copying build\lib.win32-3.6\kivy\core\window\_window_sdl2.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\core\window
copying build\lib.win32-3.6\kivy\core\window\__init__.py -> build\bdist.win32\wheel\.\kivy\core\window
copying build\lib.win32-3.6\kivy\core\__init__.py -> build\bdist.win32\wheel\.\kivy\core
creating build\bdist.win32\wheel\kivy\data
creating build\bdist.win32\wheel\kivy\data\fonts
copying build\lib.win32-3.6\kivy\data\fonts\DejaVuSans.ttf -> build\bdist.win32\wheel\.\kivy\data\fonts
copying build\lib.win32-3.6\kivy\data\fonts\Roboto-Bold.ttf -> build\bdist.win32\wheel\.\kivy\data\fonts
copying build\lib.win32-3.6\kivy\data\fonts\Roboto-BoldItalic.ttf -> build\bdist.win32\wheel\.\kivy\data\fonts
copying build\lib.win32-3.6\kivy\data\fonts\Roboto-Italic.ttf -> build\bdist.win32\wheel\.\kivy\data\fonts
copying build\lib.win32-3.6\kivy\data\fonts\Roboto-Regular.ttf -> build\bdist.win32\wheel\.\kivy\data\fonts
copying build\lib.win32-3.6\kivy\data\fonts\RobotoMono-Regular.ttf -> build\bdist.win32\wheel\.\kivy\data\fonts
creating build\bdist.win32\wheel\kivy\data\glsl
copying build\lib.win32-3.6\kivy\data\glsl\default.fs -> build\bdist.win32\wheel\.\kivy\data\glsl
copying build\lib.win32-3.6\kivy\data\glsl\default.png -> build\bdist.win32\wheel\.\kivy\data\glsl
copying build\lib.win32-3.6\kivy\data\glsl\default.vs -> build\bdist.win32\wheel\.\kivy\data\glsl
copying build\lib.win32-3.6\kivy\data\glsl\header.fs -> build\bdist.win32\wheel\.\kivy\data\glsl
copying build\lib.win32-3.6\kivy\data\glsl\header.vs -> build\bdist.win32\wheel\.\kivy\data\glsl
creating build\bdist.win32\wheel\kivy\data\images
copying build\lib.win32-3.6\kivy\data\images\background.jpg -> build\bdist.win32\wheel\.\kivy\data\images
copying build\lib.win32-3.6\kivy\data\images\cursor.png -> build\bdist.win32\wheel\.\kivy\data\images
copying build\lib.win32-3.6\kivy\data\images\defaultshape.png -> build\bdist.win32\wheel\.\kivy\data\images
copying build\lib.win32-3.6\kivy\data\images\defaulttheme-0.png -> build\bdist.win32\wheel\.\kivy\data\images
copying build\lib.win32-3.6\kivy\data\images\defaulttheme.atlas -> build\bdist.win32\wheel\.\kivy\data\images
copying build\lib.win32-3.6\kivy\data\images\image-loading.gif -> build\bdist.win32\wheel\.\kivy\data\images
copying build\lib.win32-3.6\kivy\data\images\image-loading.zip -> build\bdist.win32\wheel\.\kivy\data\images
copying build\lib.win32-3.6\kivy\data\images\testpattern.png -> build\bdist.win32\wheel\.\kivy\data\images
creating build\bdist.win32\wheel\kivy\data\keyboards
copying build\lib.win32-3.6\kivy\data\keyboards\azerty.json -> build\bdist.win32\wheel\.\kivy\data\keyboards
copying build\lib.win32-3.6\kivy\data\keyboards\de.json -> build\bdist.win32\wheel\.\kivy\data\keyboards
copying build\lib.win32-3.6\kivy\data\keyboards\de_CH.json -> build\bdist.win32\wheel\.\kivy\data\keyboards
copying build\lib.win32-3.6\kivy\data\keyboards\en_US.json -> build\bdist.win32\wheel\.\kivy\data\keyboards
copying build\lib.win32-3.6\kivy\data\keyboards\fr_CH.json -> build\bdist.win32\wheel\.\kivy\data\keyboards
copying build\lib.win32-3.6\kivy\data\keyboards\qwerty.json -> build\bdist.win32\wheel\.\kivy\data\keyboards
copying build\lib.win32-3.6\kivy\data\keyboards\qwertz.json -> build\bdist.win32\wheel\.\kivy\data\keyboards
creating build\bdist.win32\wheel\kivy\data\logo
copying build\lib.win32-3.6\kivy\data\logo\kivy-icon-128.png -> build\bdist.win32\wheel\.\kivy\data\logo
copying build\lib.win32-3.6\kivy\data\logo\kivy-icon-16.png -> build\bdist.win32\wheel\.\kivy\data\logo
copying build\lib.win32-3.6\kivy\data\logo\kivy-icon-24.png -> build\bdist.win32\wheel\.\kivy\data\logo
copying build\lib.win32-3.6\kivy\data\logo\kivy-icon-256.png -> build\bdist.win32\wheel\.\kivy\data\logo
copying build\lib.win32-3.6\kivy\data\logo\kivy-icon-32.png -> build\bdist.win32\wheel\.\kivy\data\logo
copying build\lib.win32-3.6\kivy\data\logo\kivy-icon-48.png -> build\bdist.win32\wheel\.\kivy\data\logo
copying build\lib.win32-3.6\kivy\data\logo\kivy-icon-512.png -> build\bdist.win32\wheel\.\kivy\data\logo
copying build\lib.win32-3.6\kivy\data\logo\kivy-icon-64.ico -> build\bdist.win32\wheel\.\kivy\data\logo
copying build\lib.win32-3.6\kivy\data\logo\kivy-icon-64.png -> build\bdist.win32\wheel\.\kivy\data\logo
copying build\lib.win32-3.6\kivy\data\settings_kivy.json -> build\bdist.win32\wheel\.\kivy\data
copying build\lib.win32-3.6\kivy\data\style.kv -> build\bdist.win32\wheel\.\kivy\data
creating build\bdist.win32\wheel\kivy\deps
copying build\lib.win32-3.6\kivy\deps\__init__.py -> build\bdist.win32\wheel\.\kivy\deps
creating build\bdist.win32\wheel\kivy\effects
copying build\lib.win32-3.6\kivy\effects\dampedscroll.py -> build\bdist.win32\wheel\.\kivy\effects
copying build\lib.win32-3.6\kivy\effects\kinetic.py -> build\bdist.win32\wheel\.\kivy\effects
copying build\lib.win32-3.6\kivy\effects\opacityscroll.py -> build\bdist.win32\wheel\.\kivy\effects
copying build\lib.win32-3.6\kivy\effects\scroll.py -> build\bdist.win32\wheel\.\kivy\effects
copying build\lib.win32-3.6\kivy\effects\__init__.py -> build\bdist.win32\wheel\.\kivy\effects
copying build\lib.win32-3.6\kivy\event.py -> build\bdist.win32\wheel\.\kivy
creating build\bdist.win32\wheel\kivy\extras
copying build\lib.win32-3.6\kivy\extras\highlight.py -> build\bdist.win32\wheel\.\kivy\extras
copying build\lib.win32-3.6\kivy\extras\__init__.py -> build\bdist.win32\wheel\.\kivy\extras
copying build\lib.win32-3.6\kivy\factory.py -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\factory_registers.py -> build\bdist.win32\wheel\.\kivy
creating build\bdist.win32\wheel\kivy\garden
copying build\lib.win32-3.6\kivy\garden\__init__.py -> build\bdist.win32\wheel\.\kivy\garden
copying build\lib.win32-3.6\kivy\geometry.py -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\gesture.py -> build\bdist.win32\wheel\.\kivy
creating build\bdist.win32\wheel\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\buffer.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\buffer.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\buffer.pxd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\cgl.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\cgl.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\cgl.pxd -> build\bdist.win32\wheel\.\kivy\graphics
creating build\bdist.win32\wheel\kivy\graphics\cgl_backend
copying build\lib.win32-3.6\kivy\graphics\cgl_backend\cgl_debug.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics\cgl_backend
copying build\lib.win32-3.6\kivy\graphics\cgl_backend\cgl_debug.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics\cgl_backend
copying build\lib.win32-3.6\kivy\graphics\cgl_backend\cgl_gl.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics\cgl_backend
copying build\lib.win32-3.6\kivy\graphics\cgl_backend\cgl_gl.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics\cgl_backend
copying build\lib.win32-3.6\kivy\graphics\cgl_backend\cgl_glew.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics\cgl_backend
copying build\lib.win32-3.6\kivy\graphics\cgl_backend\cgl_glew.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics\cgl_backend
copying build\lib.win32-3.6\kivy\graphics\cgl_backend\cgl_mock.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics\cgl_backend
copying build\lib.win32-3.6\kivy\graphics\cgl_backend\cgl_mock.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics\cgl_backend
copying build\lib.win32-3.6\kivy\graphics\cgl_backend\cgl_sdl2.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics\cgl_backend
copying build\lib.win32-3.6\kivy\graphics\cgl_backend\cgl_sdl2.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics\cgl_backend
copying build\lib.win32-3.6\kivy\graphics\cgl_backend\__init__.py -> build\bdist.win32\wheel\.\kivy\graphics\cgl_backend
copying build\lib.win32-3.6\kivy\graphics\common.pxi -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\compiler.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\compiler.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\compiler.pxd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\context.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\context.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\context.pxd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\context_instructions.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\context_instructions.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\context_instructions.pxd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\fbo.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\fbo.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\fbo.pxd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\gl_debug_logger.pxi -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\gl_instructions.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\gl_instructions.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\img_tools.pxi -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\instructions.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\instructions.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\instructions.pxd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\memory.pxi -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\opcodes.pxi -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\opengl.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\opengl.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\opengl_utils.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\opengl_utils.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\opengl_utils.pxd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\opengl_utils_def.pxi -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\scissor_instructions.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\scissor_instructions.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\shader.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\shader.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\shader.pxd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\stencil_instructions.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\stencil_instructions.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\stencil_instructions.pxd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\svg.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\svg.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\svg.pxd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\tesselator.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\tesselator.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\tesselator.pxd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\texture.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\texture.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\texture.pxd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\transformation.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\transformation.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\transformation.pxd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\vbo.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\vbo.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\vbo.pxd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\vertex.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\vertex.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\vertex.pxd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\vertex_instructions.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\vertex_instructions.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\vertex_instructions.pxd -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\vertex_instructions_line.pxi -> build\bdist.win32\wheel\.\kivy\graphics
copying build\lib.win32-3.6\kivy\graphics\__init__.py -> build\bdist.win32\wheel\.\kivy\graphics
creating build\bdist.win32\wheel\kivy\include
copying build\lib.win32-3.6\kivy\include\common_subset.h -> build\bdist.win32\wheel\.\kivy\include
copying build\lib.win32-3.6\kivy\include\config.h -> build\bdist.win32\wheel\.\kivy\include
copying build\lib.win32-3.6\kivy\include\config.pxi -> build\bdist.win32\wheel\.\kivy\include
copying build\lib.win32-3.6\kivy\include\gl2platform.h -> build\bdist.win32\wheel\.\kivy\include
copying build\lib.win32-3.6\kivy\include\gl_redirect.h -> build\bdist.win32\wheel\.\kivy\include
copying build\lib.win32-3.6\kivy\include\khrplatform.h -> build\bdist.win32\wheel\.\kivy\include
creating build\bdist.win32\wheel\kivy\input
copying build\lib.win32-3.6\kivy\input\factory.py -> build\bdist.win32\wheel\.\kivy\input
copying build\lib.win32-3.6\kivy\input\motionevent.py -> build\bdist.win32\wheel\.\kivy\input
creating build\bdist.win32\wheel\kivy\input\postproc
copying build\lib.win32-3.6\kivy\input\postproc\calibration.py -> build\bdist.win32\wheel\.\kivy\input\postproc
copying build\lib.win32-3.6\kivy\input\postproc\dejitter.py -> build\bdist.win32\wheel\.\kivy\input\postproc
copying build\lib.win32-3.6\kivy\input\postproc\doubletap.py -> build\bdist.win32\wheel\.\kivy\input\postproc
copying build\lib.win32-3.6\kivy\input\postproc\ignorelist.py -> build\bdist.win32\wheel\.\kivy\input\postproc
copying build\lib.win32-3.6\kivy\input\postproc\retaintouch.py -> build\bdist.win32\wheel\.\kivy\input\postproc
copying build\lib.win32-3.6\kivy\input\postproc\tripletap.py -> build\bdist.win32\wheel\.\kivy\input\postproc
copying build\lib.win32-3.6\kivy\input\postproc\__init__.py -> build\bdist.win32\wheel\.\kivy\input\postproc
copying build\lib.win32-3.6\kivy\input\provider.py -> build\bdist.win32\wheel\.\kivy\input
creating build\bdist.win32\wheel\kivy\input\providers
copying build\lib.win32-3.6\kivy\input\providers\androidjoystick.py -> build\bdist.win32\wheel\.\kivy\input\providers
copying build\lib.win32-3.6\kivy\input\providers\hidinput.py -> build\bdist.win32\wheel\.\kivy\input\providers
copying build\lib.win32-3.6\kivy\input\providers\leapfinger.py -> build\bdist.win32\wheel\.\kivy\input\providers
copying build\lib.win32-3.6\kivy\input\providers\linuxwacom.py -> build\bdist.win32\wheel\.\kivy\input\providers
copying build\lib.win32-3.6\kivy\input\providers\mactouch.py -> build\bdist.win32\wheel\.\kivy\input\providers
copying build\lib.win32-3.6\kivy\input\providers\mouse.py -> build\bdist.win32\wheel\.\kivy\input\providers
copying build\lib.win32-3.6\kivy\input\providers\mtdev.py -> build\bdist.win32\wheel\.\kivy\input\providers
copying build\lib.win32-3.6\kivy\input\providers\probesysfs.py -> build\bdist.win32\wheel\.\kivy\input\providers
copying build\lib.win32-3.6\kivy\input\providers\tuio.py -> build\bdist.win32\wheel\.\kivy\input\providers
copying build\lib.win32-3.6\kivy\input\providers\wm_common.py -> build\bdist.win32\wheel\.\kivy\input\providers
copying build\lib.win32-3.6\kivy\input\providers\wm_pen.py -> build\bdist.win32\wheel\.\kivy\input\providers
copying build\lib.win32-3.6\kivy\input\providers\wm_touch.py -> build\bdist.win32\wheel\.\kivy\input\providers
copying build\lib.win32-3.6\kivy\input\providers\__init__.py -> build\bdist.win32\wheel\.\kivy\input\providers
copying build\lib.win32-3.6\kivy\input\recorder.py -> build\bdist.win32\wheel\.\kivy\input
copying build\lib.win32-3.6\kivy\input\shape.py -> build\bdist.win32\wheel\.\kivy\input
copying build\lib.win32-3.6\kivy\input\__init__.py -> build\bdist.win32\wheel\.\kivy\input
copying build\lib.win32-3.6\kivy\interactive.py -> build\bdist.win32\wheel\.\kivy
creating build\bdist.win32\wheel\kivy\lang
copying build\lib.win32-3.6\kivy\lang\builder.py -> build\bdist.win32\wheel\.\kivy\lang
copying build\lib.win32-3.6\kivy\lang\parser.py -> build\bdist.win32\wheel\.\kivy\lang
copying build\lib.win32-3.6\kivy\lang\__init__.py -> build\bdist.win32\wheel\.\kivy\lang
creating build\bdist.win32\wheel\kivy\lib
copying build\lib.win32-3.6\kivy\lib\ddsfile.py -> build\bdist.win32\wheel\.\kivy\lib
creating build\bdist.win32\wheel\kivy\lib\gstplayer
copying build\lib.win32-3.6\kivy\lib\gstplayer\__init__.py -> build\bdist.win32\wheel\.\kivy\lib\gstplayer
copying build\lib.win32-3.6\kivy\lib\mtdev.py -> build\bdist.win32\wheel\.\kivy\lib
creating build\bdist.win32\wheel\kivy\lib\pango
copying build\lib.win32-3.6\kivy\lib\pango\pangoft2.pxi -> build\bdist.win32\wheel\.\kivy\lib\pango
copying build\lib.win32-3.6\kivy\lib\sdl2.pxi -> build\bdist.win32\wheel\.\kivy\lib
creating build\bdist.win32\wheel\kivy\lib\vidcore_lite
copying build\lib.win32-3.6\kivy\lib\vidcore_lite\bcm.pxd -> build\bdist.win32\wheel\.\kivy\lib\vidcore_lite
copying build\lib.win32-3.6\kivy\lib\vidcore_lite\__init__.py -> build\bdist.win32\wheel\.\kivy\lib\vidcore_lite
copying build\lib.win32-3.6\kivy\lib\__init__.py -> build\bdist.win32\wheel\.\kivy\lib
copying build\lib.win32-3.6\kivy\loader.py -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\logger.py -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\metrics.py -> build\bdist.win32\wheel\.\kivy
creating build\bdist.win32\wheel\kivy\modules
copying build\lib.win32-3.6\kivy\modules\console.py -> build\bdist.win32\wheel\.\kivy\modules
copying build\lib.win32-3.6\kivy\modules\cursor.py -> build\bdist.win32\wheel\.\kivy\modules
copying build\lib.win32-3.6\kivy\modules\inspector.py -> build\bdist.win32\wheel\.\kivy\modules
copying build\lib.win32-3.6\kivy\modules\joycursor.py -> build\bdist.win32\wheel\.\kivy\modules
copying build\lib.win32-3.6\kivy\modules\keybinding.py -> build\bdist.win32\wheel\.\kivy\modules
copying build\lib.win32-3.6\kivy\modules\monitor.py -> build\bdist.win32\wheel\.\kivy\modules
copying build\lib.win32-3.6\kivy\modules\recorder.py -> build\bdist.win32\wheel\.\kivy\modules
copying build\lib.win32-3.6\kivy\modules\screen.py -> build\bdist.win32\wheel\.\kivy\modules
copying build\lib.win32-3.6\kivy\modules\showborder.py -> build\bdist.win32\wheel\.\kivy\modules
copying build\lib.win32-3.6\kivy\modules\touchring.py -> build\bdist.win32\wheel\.\kivy\modules
copying build\lib.win32-3.6\kivy\modules\webdebugger.py -> build\bdist.win32\wheel\.\kivy\modules
copying build\lib.win32-3.6\kivy\modules\_webdebugger.py -> build\bdist.win32\wheel\.\kivy\modules
copying build\lib.win32-3.6\kivy\modules\__init__.py -> build\bdist.win32\wheel\.\kivy\modules
copying build\lib.win32-3.6\kivy\multistroke.py -> build\bdist.win32\wheel\.\kivy
creating build\bdist.win32\wheel\kivy\network
copying build\lib.win32-3.6\kivy\network\urlrequest.py -> build\bdist.win32\wheel\.\kivy\network
copying build\lib.win32-3.6\kivy\network\__init__.py -> build\bdist.win32\wheel\.\kivy\network
copying build\lib.win32-3.6\kivy\parser.py -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\properties.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\properties.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\properties.pxd -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\resources.py -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\setupconfig.py -> build\bdist.win32\wheel\.\kivy
creating build\bdist.win32\wheel\kivy\storage
copying build\lib.win32-3.6\kivy\storage\dictstore.py -> build\bdist.win32\wheel\.\kivy\storage
copying build\lib.win32-3.6\kivy\storage\jsonstore.py -> build\bdist.win32\wheel\.\kivy\storage
copying build\lib.win32-3.6\kivy\storage\redisstore.py -> build\bdist.win32\wheel\.\kivy\storage
copying build\lib.win32-3.6\kivy\storage\__init__.py -> build\bdist.win32\wheel\.\kivy\storage
copying build\lib.win32-3.6\kivy\support.py -> build\bdist.win32\wheel\.\kivy
creating build\bdist.win32\wheel\kivy\tests
copying build\lib.win32-3.6\kivy\tests\async_common.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\common.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\conftest.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\coverage_lang.kv -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\fixtures.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\perf_test_textinput.py -> build\bdist.win32\wheel\.\kivy\tests
creating build\bdist.win32\wheel\kivy\tests\pyinstaller
creating build\bdist.win32\wheel\kivy\tests\pyinstaller\simple_widget
copying build\lib.win32-3.6\kivy\tests\pyinstaller\simple_widget\main.py -> build\bdist.win32\wheel\.\kivy\tests\pyinstaller\simple_widget
copying build\lib.win32-3.6\kivy\tests\pyinstaller\simple_widget\main.spec -> build\bdist.win32\wheel\.\kivy\tests\pyinstaller\simple_widget
creating build\bdist.win32\wheel\kivy\tests\pyinstaller\simple_widget\project
copying build\lib.win32-3.6\kivy\tests\pyinstaller\simple_widget\project\widget.py -> build\bdist.win32\wheel\.\kivy\tests\pyinstaller\simple_widget\project
copying build\lib.win32-3.6\kivy\tests\pyinstaller\simple_widget\project\__init__.py -> build\bdist.win32\wheel\.\kivy\tests\pyinstaller\simple_widget\project
copying build\lib.win32-3.6\kivy\tests\pyinstaller\test_pyinstaller.py -> build\bdist.win32\wheel\.\kivy\tests\pyinstaller
creating build\bdist.win32\wheel\kivy\tests\pyinstaller\video_widget
copying build\lib.win32-3.6\kivy\tests\pyinstaller\video_widget\main.py -> build\bdist.win32\wheel\.\kivy\tests\pyinstaller\video_widget
copying build\lib.win32-3.6\kivy\tests\pyinstaller\video_widget\main.spec -> build\bdist.win32\wheel\.\kivy\tests\pyinstaller\video_widget
creating build\bdist.win32\wheel\kivy\tests\pyinstaller\video_widget\project
copying build\lib.win32-3.6\kivy\tests\pyinstaller\video_widget\project\__init__.py -> build\bdist.win32\wheel\.\kivy\tests\pyinstaller\video_widget\project
copying build\lib.win32-3.6\kivy\tests\sample1.ogg -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\testkv.kv -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_animations.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_app.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_audio.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_button.png -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_clipboard.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_clock.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_coverage.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_doc_gallery.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_fbo_py2py3.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_filechooser.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_filechooser_unicode.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_fonts.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_graphics.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_image.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_imageloader.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_invalid_lang.py -> build\bdist.win32\wheel\.\kivy\tests
creating build\bdist.win32\wheel\kivy\tests\test_issues
copying build\lib.win32-3.6\kivy\tests\test_issues\test_6315.py -> build\bdist.win32\wheel\.\kivy\tests\test_issues
copying build\lib.win32-3.6\kivy\tests\test_issues\test_issue_1084.py -> build\bdist.win32\wheel\.\kivy\tests\test_issues
copying build\lib.win32-3.6\kivy\tests\test_issues\test_issue_1091.py -> build\bdist.win32\wheel\.\kivy\tests\test_issues
copying build\lib.win32-3.6\kivy\tests\test_issues\test_issue_599.py -> build\bdist.win32\wheel\.\kivy\tests\test_issues
copying build\lib.win32-3.6\kivy\tests\test_issues\test_issue_609.py -> build\bdist.win32\wheel\.\kivy\tests\test_issues
copying build\lib.win32-3.6\kivy\tests\test_issues\test_issue_6909.py -> build\bdist.win32\wheel\.\kivy\tests\test_issues
copying build\lib.win32-3.6\kivy\tests\test_issues\test_issue_883.py -> build\bdist.win32\wheel\.\kivy\tests\test_issues
copying build\lib.win32-3.6\kivy\tests\test_knspace.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_lang.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_lang_complex.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_lang_pre_process_and_post_process.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_module_inspector.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_mouse_multitouchsim.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_multistroke.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_properties.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_rst_replace.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_screen.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_storage.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_uix_actionbar.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_uix_anchorlayout.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_uix_asyncimage.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_uix_boxlayout.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_uix_bubble.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_uix_carousel.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_uix_dropdown.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_uix_gridlayout.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_uix_layout.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_uix_modal.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_uix_relativelayout.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_uix_scrollview.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_uix_slider.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_uix_stacklayout.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_uix_textinput.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_uix_translate_coordinates.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_uix_widget.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_urlrequest.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_utils.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_vector.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_video.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_weakmethod.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_widget.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_widget_walk.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\test_window_info.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\unicode_files.zip -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\unicode_font.zip -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\visual_test_label.py -> build\bdist.win32\wheel\.\kivy\tests
copying build\lib.win32-3.6\kivy\tests\__init__.py -> build\bdist.win32\wheel\.\kivy\tests
creating build\bdist.win32\wheel\kivy\tools
copying build\lib.win32-3.6\kivy\tools\benchmark.py -> build\bdist.win32\wheel\.\kivy\tools
copying build\lib.win32-3.6\kivy\tools\changelog_parser.py -> build\bdist.win32\wheel\.\kivy\tools
copying build\lib.win32-3.6\kivy\tools\coverage.py -> build\bdist.win32\wheel\.\kivy\tools
copying build\lib.win32-3.6\kivy\tools\gallery.py -> build\bdist.win32\wheel\.\kivy\tools
copying build\lib.win32-3.6\kivy\tools\generate-icons.py -> build\bdist.win32\wheel\.\kivy\tools
creating build\bdist.win32\wheel\kivy\tools\gles_compat
copying build\lib.win32-3.6\kivy\tools\gles_compat\gl2.h -> build\bdist.win32\wheel\.\kivy\tools\gles_compat
copying build\lib.win32-3.6\kivy\tools\gles_compat\subset_gles.py -> build\bdist.win32\wheel\.\kivy\tools\gles_compat
creating build\bdist.win32\wheel\kivy\tools\highlight
copying build\lib.win32-3.6\kivy\tools\highlight\kivy-mode.el -> build\bdist.win32\wheel\.\kivy\tools\highlight
copying build\lib.win32-3.6\kivy\tools\highlight\kivy.json-tmlanguage -> build\bdist.win32\wheel\.\kivy\tools\highlight
copying build\lib.win32-3.6\kivy\tools\highlight\kivy.tmLanguage -> build\bdist.win32\wheel\.\kivy\tools\highlight
copying build\lib.win32-3.6\kivy\tools\highlight\kivy.vim -> build\bdist.win32\wheel\.\kivy\tools\highlight
copying build\lib.win32-3.6\kivy\tools\highlight\__init__.py -> build\bdist.win32\wheel\.\kivy\tools\highlight
creating build\bdist.win32\wheel\kivy\tools\image-testsuite
copying build\lib.win32-3.6\kivy\tools\image-testsuite\gimp28-testsuite.py -> build\bdist.win32\wheel\.\kivy\tools\image-testsuite
copying build\lib.win32-3.6\kivy\tools\image-testsuite\imagemagick-testsuite.sh -> build\bdist.win32\wheel\.\kivy\tools\image-testsuite
copying build\lib.win32-3.6\kivy\tools\image-testsuite\README.md -> build\bdist.win32\wheel\.\kivy\tools\image-testsuite
copying build\lib.win32-3.6\kivy\tools\kviewer.py -> build\bdist.win32\wheel\.\kivy\tools
creating build\bdist.win32\wheel\kivy\tools\packaging
copying build\lib.win32-3.6\kivy\tools\packaging\cython_cfg.py -> build\bdist.win32\wheel\.\kivy\tools\packaging
copying build\lib.win32-3.6\kivy\tools\packaging\factory.py -> build\bdist.win32\wheel\.\kivy\tools\packaging
creating build\bdist.win32\wheel\kivy\tools\packaging\pyinstaller_hooks
copying build\lib.win32-3.6\kivy\tools\packaging\pyinstaller_hooks\hook-kivy.py -> build\bdist.win32\wheel\.\kivy\tools\packaging\pyinstaller_hooks
copying build\lib.win32-3.6\kivy\tools\packaging\pyinstaller_hooks\pyi_rth_kivy.py -> build\bdist.win32\wheel\.\kivy\tools\packaging\pyinstaller_hooks
copying build\lib.win32-3.6\kivy\tools\packaging\pyinstaller_hooks\__init__.py -> build\bdist.win32\wheel\.\kivy\tools\packaging\pyinstaller_hooks
copying build\lib.win32-3.6\kivy\tools\packaging\pyinstaller_hooks\__main__.py -> build\bdist.win32\wheel\.\kivy\tools\packaging\pyinstaller_hooks
copying build\lib.win32-3.6\kivy\tools\packaging\__init__.py -> build\bdist.win32\wheel\.\kivy\tools\packaging
creating build\bdist.win32\wheel\kivy\tools\pep8checker
copying build\lib.win32-3.6\kivy\tools\pep8checker\pep8.py -> build\bdist.win32\wheel\.\kivy\tools\pep8checker
copying build\lib.win32-3.6\kivy\tools\pep8checker\pep8kivy.py -> build\bdist.win32\wheel\.\kivy\tools\pep8checker
copying build\lib.win32-3.6\kivy\tools\pep8checker\pre-commit.githook -> build\bdist.win32\wheel\.\kivy\tools\pep8checker
copying build\lib.win32-3.6\kivy\tools\report.py -> build\bdist.win32\wheel\.\kivy\tools
copying build\lib.win32-3.6\kivy\tools\stub-gl-debug.py -> build\bdist.win32\wheel\.\kivy\tools
copying build\lib.win32-3.6\kivy\tools\texturecompress.py -> build\bdist.win32\wheel\.\kivy\tools
creating build\bdist.win32\wheel\kivy\tools\theming
creating build\bdist.win32\wheel\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\action_bar.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\action_group.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\action_group_disabled.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\action_group_down.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\action_item.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\action_item_down.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\action_view.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\audio-volume-high.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\audio-volume-low.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\audio-volume-medium.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\audio-volume-muted.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\bubble.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\bubble_arrow.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\bubble_btn.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\bubble_btn_pressed.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\button.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\button_disabled.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\button_disabled_pressed.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\button_pressed.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\checkbox_disabled_off.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\checkbox_disabled_on.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\checkbox_off.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\checkbox_on.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\checkbox_radio_disabled_off.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\checkbox_radio_disabled_on.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\checkbox_radio_off.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\checkbox_radio_on.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\close.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\filechooser_file.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\filechooser_folder.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\filechooser_selected.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\image-missing.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\media-playback-pause.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\media-playback-start.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\media-playback-stop.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\modalview-background.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\overflow.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\player-background.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\player-play-overlay.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\previous_normal.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\progressbar.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\progressbar_background.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\ring.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\selector_left.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\selector_middle.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\selector_right.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\separator.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\sliderh_background.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\sliderh_background_disabled.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\sliderv_background.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\sliderv_background_disabled.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\slider_cursor.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\slider_cursor_disabled.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\spinner.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\spinner_disabled.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\spinner_pressed.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\splitter.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\splitter_disabled.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\splitter_disabled_down.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\splitter_disabled_down_h.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\splitter_disabled_h.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\splitter_down.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\splitter_down_h.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\splitter_grip.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\splitter_grip_h.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\splitter_h.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\switch-background.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\switch-background_disabled.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\switch-button.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\switch-button_disabled.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\tab.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\tab_btn.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\tab_btn_disabled.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\tab_btn_disabled_pressed.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\tab_btn_pressed.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\tab_disabled.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\textinput.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\textinput_active.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\textinput_disabled.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\textinput_disabled_active.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\tree_closed.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\tree_opened.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\vkeyboard_background.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\vkeyboard_disabled_background.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\vkeyboard_disabled_key_down.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\vkeyboard_disabled_key_normal.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\vkeyboard_key_down.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\theming\defaulttheme\vkeyboard_key_normal.png -> build\bdist.win32\wheel\.\kivy\tools\theming\defaulttheme
copying build\lib.win32-3.6\kivy\tools\__init__.py -> build\bdist.win32\wheel\.\kivy\tools
creating build\bdist.win32\wheel\kivy\uix
copying build\lib.win32-3.6\kivy\uix\accordion.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\actionbar.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\anchorlayout.py -> build\bdist.win32\wheel\.\kivy\uix
creating build\bdist.win32\wheel\kivy\uix\behaviors
copying build\lib.win32-3.6\kivy\uix\behaviors\button.py -> build\bdist.win32\wheel\.\kivy\uix\behaviors
copying build\lib.win32-3.6\kivy\uix\behaviors\codenavigation.py -> build\bdist.win32\wheel\.\kivy\uix\behaviors
copying build\lib.win32-3.6\kivy\uix\behaviors\compoundselection.py -> build\bdist.win32\wheel\.\kivy\uix\behaviors
copying build\lib.win32-3.6\kivy\uix\behaviors\cover.py -> build\bdist.win32\wheel\.\kivy\uix\behaviors
copying build\lib.win32-3.6\kivy\uix\behaviors\drag.py -> build\bdist.win32\wheel\.\kivy\uix\behaviors
copying build\lib.win32-3.6\kivy\uix\behaviors\emacs.py -> build\bdist.win32\wheel\.\kivy\uix\behaviors
copying build\lib.win32-3.6\kivy\uix\behaviors\focus.py -> build\bdist.win32\wheel\.\kivy\uix\behaviors
copying build\lib.win32-3.6\kivy\uix\behaviors\knspace.py -> build\bdist.win32\wheel\.\kivy\uix\behaviors
copying build\lib.win32-3.6\kivy\uix\behaviors\togglebutton.py -> build\bdist.win32\wheel\.\kivy\uix\behaviors
copying build\lib.win32-3.6\kivy\uix\behaviors\touchripple.py -> build\bdist.win32\wheel\.\kivy\uix\behaviors
copying build\lib.win32-3.6\kivy\uix\behaviors\__init__.py -> build\bdist.win32\wheel\.\kivy\uix\behaviors
copying build\lib.win32-3.6\kivy\uix\boxlayout.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\bubble.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\button.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\camera.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\carousel.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\checkbox.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\codeinput.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\colorpicker.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\dropdown.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\effectwidget.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\filechooser.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\floatlayout.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\gesturesurface.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\gridlayout.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\image.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\label.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\layout.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\modalview.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\pagelayout.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\popup.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\progressbar.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\recycleboxlayout.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\recyclegridlayout.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\recyclelayout.py -> build\bdist.win32\wheel\.\kivy\uix
creating build\bdist.win32\wheel\kivy\uix\recycleview
copying build\lib.win32-3.6\kivy\uix\recycleview\datamodel.py -> build\bdist.win32\wheel\.\kivy\uix\recycleview
copying build\lib.win32-3.6\kivy\uix\recycleview\layout.py -> build\bdist.win32\wheel\.\kivy\uix\recycleview
copying build\lib.win32-3.6\kivy\uix\recycleview\views.py -> build\bdist.win32\wheel\.\kivy\uix\recycleview
copying build\lib.win32-3.6\kivy\uix\recycleview\__init__.py -> build\bdist.win32\wheel\.\kivy\uix\recycleview
copying build\lib.win32-3.6\kivy\uix\relativelayout.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\rst.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\sandbox.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\scatter.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\scatterlayout.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\screenmanager.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\scrollview.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\settings.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\slider.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\spinner.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\splitter.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\stacklayout.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\stencilview.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\switch.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\tabbedpanel.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\textinput.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\togglebutton.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\treeview.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\video.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\videoplayer.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\vkeyboard.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\widget.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\uix\__init__.py -> build\bdist.win32\wheel\.\kivy\uix
copying build\lib.win32-3.6\kivy\utils.py -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\vector.py -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\weakmethod.py -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\weakproxy.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\weakproxy.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\_clock.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\_clock.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\_clock.pxd -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\_event.cp36-win32.pdb -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\_event.cp36-win32.pyd -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\_event.pxd -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\_version.py -> build\bdist.win32\wheel\.\kivy
copying build\lib.win32-3.6\kivy\__init__.py -> build\bdist.win32\wheel\.\kivy
running install_data
creating build\bdist.win32\wheel\Kivy-2.0.0.data
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\3Drendering
copying examples\3Drendering\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\3Drendering
copying examples\3Drendering\monkey.obj -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\3Drendering
copying examples\3Drendering\objloader.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\3Drendering
copying examples\3Drendering\simple.glsl -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\3Drendering
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\android
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\android\compass
copying examples\android\compass\android.txt -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\android\compass
copying examples\android\compass\compass.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\android\compass
copying examples\android\compass\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\android\compass
copying examples\android\compass\needle.png -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\android\compass
copying examples\android\compass\rose.png -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\android\compass
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\android\takepicture
copying examples\android\takepicture\android.txt -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\android\takepicture
copying examples\android\takepicture\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\android\takepicture
copying examples\android\takepicture\shadow32.png -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\android\takepicture
copying examples\android\takepicture\takepicture.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\android\takepicture
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\animation
copying examples\animation\animate.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\animation
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\application
copying examples\application\app_suite.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\application
copying examples\application\app_with_build.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\application
copying examples\application\app_with_config.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\application
copying examples\application\app_with_kv.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\application
copying examples\application\app_with_kv_in_template1.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\application
copying examples\application\test.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\application
copying examples\application\testkvfile.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\application
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\application\app_suite_data
copying examples\application\app_suite_data\testkvdir.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\application\app_suite_data
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\application\template1
copying examples\application\template1\test.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\application\template1
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\async
copying examples\async\asyncio_advanced.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\async
copying examples\async\asyncio_basic.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\async
copying examples\async\trio_advanced.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\async
copying examples\async\trio_basic.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\async
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
copying examples\audio\12908_sweet_trip_mm_clap_hi.wav -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
copying examples\audio\12909_sweet_trip_mm_clap_lo.wav -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
copying examples\audio\12910_sweet_trip_mm_clap_mid.wav -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
copying examples\audio\12911_sweet_trip_mm_hat_cl.wav -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
copying examples\audio\12913_sweet_trip_mm_kick_hi.wav -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
copying examples\audio\12914_sweet_trip_mm_kick_lo.wav -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
copying examples\audio\12915_sweet_trip_mm_kick_mid.wav -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
copying examples\audio\12916_sweet_trip_mm_kwik_mod_01.wav -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
copying examples\audio\12917_sweet_trip_mm_kwik_mod_02.wav -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
copying examples\audio\12918_sweet_trip_mm_kwik_mod_03.wav -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
copying examples\audio\12919_sweet_trip_mm_kwik_mod_04.wav -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
copying examples\audio\12920_sweet_trip_mm_kwik_mod_05.wav -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
copying examples\audio\12921_sweet_trip_mm_kwik_mod_06.wav -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
copying examples\audio\12922_sweet_trip_mm_kwik_mod_07.wav -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
copying examples\audio\12923_sweet_trip_mm_metal_clave.wav -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
copying examples\audio\12925_sweet_trip_mm_sweep_x.wav -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
copying examples\audio\12926_sweet_trip_mm_sweep_y.wav -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
copying examples\audio\12927_sweet_trip_mm_sweep_z.wav -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
copying examples\audio\audio.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
copying examples\audio\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
copying examples\audio\pitch.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\audio
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\camera
copying examples\camera\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\camera
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\canvas
copying examples\canvas\bezier.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\canvas
copying examples\canvas\canvas_stress.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\canvas
copying examples\canvas\circle.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\canvas
copying examples\canvas\fbo_canvas.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\canvas
copying examples\canvas\kiwi.jpg -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\canvas
copying examples\canvas\lines.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\canvas
copying examples\canvas\lines_extended.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\canvas
copying examples\canvas\mesh.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\canvas
copying examples\canvas\mesh_manipulation.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\canvas
copying examples\canvas\mtexture1.png -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\canvas
copying examples\canvas\mtexture2.png -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\canvas
copying examples\canvas\multitexture.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\canvas
copying examples\canvas\repeat_texture.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\canvas
copying examples\canvas\rotation.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\canvas
copying examples\canvas\rounded_rectangle.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\canvas
copying examples\canvas\scale.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\canvas
copying examples\canvas\stencil_canvas.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\canvas
copying examples\canvas\tesselate.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\canvas
copying examples\canvas\texture.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\canvas
copying examples\canvas\texture_example_image.png -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\canvas
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\container
copying examples\container\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\container
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\container\kv
copying examples\container\kv\1.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\container\kv
copying examples\container\kv\2.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\container\kv
copying examples\container\kv\3.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\container\kv
copying examples\container\kv\root.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\container\kv
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\cover
copying examples\cover\cover_image.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\cover
copying examples\cover\cover_video.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\cover
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo
copying examples\demo\camera_puzzle.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\kivycatalog
copying examples\demo\kivycatalog\kivycatalog.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\kivycatalog
copying examples\demo\kivycatalog\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\kivycatalog
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\kivycatalog\container_kvs
copying examples\demo\kivycatalog\container_kvs\AnchorLayoutContainer.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\kivycatalog\container_kvs
copying examples\demo\kivycatalog\container_kvs\BoxLayoutContainer.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\kivycatalog\container_kvs
copying examples\demo\kivycatalog\container_kvs\ButtonContainer.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\kivycatalog\container_kvs
copying examples\demo\kivycatalog\container_kvs\CheckBoxContainer.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\kivycatalog\container_kvs
copying examples\demo\kivycatalog\container_kvs\FileChooserContainer.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\kivycatalog\container_kvs
copying examples\demo\kivycatalog\container_kvs\FloatLayoutContainer.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\kivycatalog\container_kvs
copying examples\demo\kivycatalog\container_kvs\GridLayoutContainer.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\kivycatalog\container_kvs
copying examples\demo\kivycatalog\container_kvs\LabelContainer.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\kivycatalog\container_kvs
copying examples\demo\kivycatalog\container_kvs\MediaContainer.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\kivycatalog\container_kvs
copying examples\demo\kivycatalog\container_kvs\PlaygroundContainer.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\kivycatalog\container_kvs
copying examples\demo\kivycatalog\container_kvs\PopupContainer.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\kivycatalog\container_kvs
copying examples\demo\kivycatalog\container_kvs\ProgressBarContainer.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\kivycatalog\container_kvs
copying examples\demo\kivycatalog\container_kvs\RestContainer.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\kivycatalog\container_kvs
copying examples\demo\kivycatalog\container_kvs\ScatterContainer.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\kivycatalog\container_kvs
copying examples\demo\kivycatalog\container_kvs\SelectorsContainer.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\kivycatalog\container_kvs
copying examples\demo\kivycatalog\container_kvs\StackLayoutContainer.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\kivycatalog\container_kvs
copying examples\demo\kivycatalog\container_kvs\TextContainer.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\kivycatalog\container_kvs
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\multistroke
copying examples\demo\multistroke\gesturedatabase.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\multistroke
copying examples\demo\multistroke\gesturedatabase.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\multistroke
copying examples\demo\multistroke\helpers.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\multistroke
copying examples\demo\multistroke\historymanager.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\multistroke
copying examples\demo\multistroke\historymanager.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\multistroke
copying examples\demo\multistroke\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\multistroke
copying examples\demo\multistroke\multistroke.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\multistroke
copying examples\demo\multistroke\settings.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\multistroke
copying examples\demo\multistroke\settings.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\multistroke
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\pictures
copying examples\demo\pictures\android.txt -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\pictures
copying examples\demo\pictures\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\pictures
copying examples\demo\pictures\pictures.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\pictures
copying examples\demo\pictures\shadow32.png -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\pictures
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\pictures\images
copying examples\demo\pictures\images\Bubbles.jpg -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\pictures\images
copying examples\demo\pictures\images\faust_github.jpg -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\pictures\images
copying examples\demo\pictures\images\Ill1.jpg -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\pictures\images
copying examples\demo\pictures\images\Wall.jpg -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\pictures\images
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\shadereditor
copying examples\demo\shadereditor\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\shadereditor
copying examples\demo\shadereditor\shadereditor.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\shadereditor
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase
copying examples\demo\showcase\android.txt -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase
copying examples\demo\showcase\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase
copying examples\demo\showcase\README.txt -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase
copying examples\demo\showcase\showcase.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data
copying examples\demo\showcase\data\background.png -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data
copying examples\demo\showcase\data\faust_github.jpg -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\icons
copying examples\demo\showcase\data\icons\bug.png -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\icons
copying examples\demo\showcase\data\icons\chevron-left.png -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\icons
copying examples\demo\showcase\data\icons\chevron-right.png -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\icons
copying examples\demo\showcase\data\icons\README -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\icons
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\screens
copying examples\demo\showcase\data\screens\accordions.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\screens
copying examples\demo\showcase\data\screens\bubbles.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\screens
copying examples\demo\showcase\data\screens\buttons.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\screens
copying examples\demo\showcase\data\screens\carousel.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\screens
copying examples\demo\showcase\data\screens\checkboxes.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\screens
copying examples\demo\showcase\data\screens\codeinput.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\screens
copying examples\demo\showcase\data\screens\dropdown.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\screens
copying examples\demo\showcase\data\screens\filechoosers.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\screens
copying examples\demo\showcase\data\screens\popups.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\screens
copying examples\demo\showcase\data\screens\progressbar.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\screens
copying examples\demo\showcase\data\screens\rstdocument.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\screens
copying examples\demo\showcase\data\screens\scatter.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\screens
copying examples\demo\showcase\data\screens\screenmanager.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\screens
copying examples\demo\showcase\data\screens\sliders.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\screens
copying examples\demo\showcase\data\screens\spinner.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\screens
copying examples\demo\showcase\data\screens\splitter.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\screens
copying examples\demo\showcase\data\screens\switches.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\screens
copying examples\demo\showcase\data\screens\tabbedpanel + layouts.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\screens
copying examples\demo\showcase\data\screens\textinputs.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\screens
copying examples\demo\showcase\data\screens\togglebutton.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\showcase\data\screens
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\touchtracer
copying examples\demo\touchtracer\android.txt -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\touchtracer
copying examples\demo\touchtracer\icon.png -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\touchtracer
copying examples\demo\touchtracer\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\touchtracer
copying examples\demo\touchtracer\particle.png -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\touchtracer
copying examples\demo\touchtracer\README.txt -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\touchtracer
copying examples\demo\touchtracer\touchtracer.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\demo\touchtracer
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\frameworks
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\frameworks\twisted
copying examples\frameworks\twisted\echo_client_app.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\frameworks\twisted
copying examples\frameworks\twisted\echo_server_app.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\frameworks\twisted
copying examples\frameworks\twisted\twistd_app.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\frameworks\twisted
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\gestures
copying examples\gestures\gesture_board.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\gestures
copying examples\gestures\my_gestures.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\gestures
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\guide
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\guide\designwithkv
copying examples\guide\designwithkv\controller.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\guide\designwithkv
copying examples\guide\designwithkv\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\guide\designwithkv
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\guide\firstwidget
copying examples\guide\firstwidget\1_skeleton.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\guide\firstwidget
copying examples\guide\firstwidget\2_print_touch.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\guide\firstwidget
copying examples\guide\firstwidget\3_draw_ellipse.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\guide\firstwidget
copying examples\guide\firstwidget\4_draw_line.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\guide\firstwidget
copying examples\guide\firstwidget\5_random_colors.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\guide\firstwidget
copying examples\guide\firstwidget\6_button.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\guide\firstwidget
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\guide\quickstart
copying examples\guide\quickstart\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\guide\quickstart
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\includes
copying examples\includes\button.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\includes
copying examples\includes\layout.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\includes
copying examples\includes\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\includes
copying examples\includes\test.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\includes
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\keyboard
copying examples\keyboard\android.txt -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\keyboard
copying examples\keyboard\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\keyboard
copying examples\keyboard\numeric.json -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\keyboard
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kinect
copying examples\kinect\kinectviewer.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kinect
copying examples\kinect\README.txt -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kinect
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kv
copying examples\kv\app_button.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kv
copying examples\kv\app_camera.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kv
copying examples\kv\app_fbo.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kv
copying examples\kv\app_layout.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kv
copying examples\kv\app_logo.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kv
copying examples\kv\app_scatter.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kv
copying examples\kv\app_stencil.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kv
copying examples\kv\app_video.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kv
copying examples\kv\builder_template.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kv
copying examples\kv\kivy.jpg -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kv
copying examples\kv\kvrun.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kv
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kv\ids
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kv\ids\id_in_kv
copying examples\kv\ids\id_in_kv\id_in_kv.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kv\ids\id_in_kv
copying examples\kv\ids\id_in_kv\test.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kv\ids\id_in_kv
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kv\ids\kv_and_py
copying examples\kv\ids\kv_and_py\kv_and_py.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kv\ids\kv_and_py
copying examples\kv\ids\kv_and_py\test.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\kv\ids\kv_and_py
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\miscellaneous
copying examples\miscellaneous\clipboard.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\miscellaneous
copying examples\miscellaneous\imagesave.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\miscellaneous
copying examples\miscellaneous\joystick.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\miscellaneous
copying examples\miscellaneous\multiple_dropfile.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\miscellaneous
copying examples\miscellaneous\on_textedit_event.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\miscellaneous
copying examples\miscellaneous\shapecollisions.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\miscellaneous
copying examples\miscellaneous\shapedwindow.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\miscellaneous
copying examples\miscellaneous\two_panes.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\miscellaneous
copying examples\miscellaneous\urlrequest.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\miscellaneous
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\RST_Editor
copying examples\RST_Editor\editor.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\RST_Editor
copying examples\RST_Editor\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\RST_Editor
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\settings
copying examples\settings\android.txt -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\settings
copying examples\settings\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\settings
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\shader
copying examples\shader\plasma.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\shader
copying examples\shader\plasma.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\shader
copying examples\shader\rotated.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\shader
copying examples\shader\rotated.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\shader
copying examples\shader\shadertree.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\shader
copying examples\shader\shadertree.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\shader
copying examples\shader\tex3.jpg -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\shader
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\svg
copying examples\svg\benchmark.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\svg
copying examples\svg\cloud.svg -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\svg
copying examples\svg\main-smaa.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\svg
copying examples\svg\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\svg
copying examples\svg\music.svg -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\svg
copying examples\svg\ship.svg -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\svg
copying examples\svg\sun.svg -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\svg
copying examples\svg\tiger.svg -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\svg
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\text
copying examples\text\pango_demo.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\text
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\notes
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\notes\final
copying examples\tutorials\notes\final\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\notes\final
copying examples\tutorials\notes\final\note.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\notes\final
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\notes\final\data
copying examples\tutorials\notes\final\data\icon.png -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\notes\final\data
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\pong
copying examples\tutorials\pong\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\pong
copying examples\tutorials\pong\pong.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\pong
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\pong\steps
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\pong\steps\step1
copying examples\tutorials\pong\steps\step1\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\pong\steps\step1
copying examples\tutorials\pong\steps\step1\pong.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\pong\steps\step1
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\pong\steps\step2
copying examples\tutorials\pong\steps\step2\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\pong\steps\step2
copying examples\tutorials\pong\steps\step2\pong.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\pong\steps\step2
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\pong\steps\step3
copying examples\tutorials\pong\steps\step3\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\pong\steps\step3
copying examples\tutorials\pong\steps\step3\pong.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\pong\steps\step3
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\pong\steps\step4
copying examples\tutorials\pong\steps\step4\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\pong\steps\step4
copying examples\tutorials\pong\steps\step4\pong.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\pong\steps\step4
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\pong\steps\step5
copying examples\tutorials\pong\steps\step5\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\pong\steps\step5
copying examples\tutorials\pong\steps\step5\pong.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\tutorials\pong\steps\step5
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\accordion_1.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\actionbar.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\asyncimage.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\boxlayout_poshint.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\bubble_test.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\camera.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\carousel_buttons.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\cityCC0.mpg -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\cityCC0.png -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\codeinput.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\codeinputtest.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\colorpicker.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\colorusage.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\compound_selection.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\customcollide.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\effectwidget.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\effectwidget2.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\effectwidget3_advanced.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\fbowidget.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\focus_behavior.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\image_mipmap.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\keyboardlistener.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\label_mipmap.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\label_sizing.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\label_text_size.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\label_with_markup.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\lang_dynamic_classes.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\pagelayout.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\popup_with_kv.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\rstexample.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\scatter.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\scatter.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\screenmanager.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\scrollview.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\scrollview.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\settings.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\shorten_text.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\spinner.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\splitter.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\tabbedpanel.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\tabbed_panel_showcase.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\textalign.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\textalign.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\textinput.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\unicode_textinput.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
copying examples\widgets\videoplayer.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\recycleview
copying examples\widgets\recycleview\basic_data.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\recycleview
copying examples\widgets\recycleview\infinite_scrolling.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\recycleview
copying examples\widgets\recycleview\key_viewclass.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\recycleview
copying examples\widgets\recycleview\messenger.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\recycleview
copying examples\widgets\recycleview\pull_to_refresh.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\recycleview
copying examples\widgets\recycleview\rv_animate_items.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\recycleview
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\sequenced_images
copying examples\widgets\sequenced_images\android.txt -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\sequenced_images
copying examples\widgets\sequenced_images\main.kv -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\sequenced_images
copying examples\widgets\sequenced_images\main.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\sequenced_images
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\sequenced_images\data
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\sequenced_images\data\images
copying examples\widgets\sequenced_images\data\images\bird.zip -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\sequenced_images\data\images
copying examples\widgets\sequenced_images\data\images\button_white.png -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\sequenced_images\data\images
copying examples\widgets\sequenced_images\data\images\button_white_animated.zip -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\sequenced_images\data\images
copying examples\widgets\sequenced_images\data\images\cube.zip -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\sequenced_images\data\images
copying examples\widgets\sequenced_images\data\images\info.png -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\sequenced_images\data\images
copying examples\widgets\sequenced_images\data\images\info.zip -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\sequenced_images\data\images
copying examples\widgets\sequenced_images\data\images\simple_cv_joint_animated.gif -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\sequenced_images\data\images
creating build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\sequenced_images\uix
copying examples\widgets\sequenced_images\uix\custom_button.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\sequenced_images\uix
copying examples\widgets\sequenced_images\uix\__init__.py -> build\bdist.win32\wheel\Kivy-2.0.0.data\data\share\kivy-examples\widgets\sequenced_images\uix
running install_egg_info
running egg_info
writing Kivy.egg-info\PKG-INFO
writing dependency_links to Kivy.egg-info\dependency_links.txt
writing requirements to Kivy.egg-info\requires.txt
writing top-level names to Kivy.egg-info\top_level.txt
reading manifest file 'Kivy.egg-info\SOURCES.txt'
reading manifest template 'MANIFEST.in'
 warning: no files found matching '*' under directory 'doc'
 warning: no files found matching '*.txt' under directory 'kivy\tools'
 warning: no files found matching '*.bat' under directory 'kivy\tools'
 warning: no files found matching '*.pyd' under directory 'kivy'
adding license file 'LICENSE'
adding license file 'AUTHORS'
writing manifest file 'Kivy.egg-info\SOURCES.txt'
Copying Kivy.egg-info to build\bdist.win32\wheel\.\Kivy-2.0.0-py3.6.egg-info
running install_scripts
 C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages\wheel\bdist_wheel.py:82: RuntimeWarning: Config variable 'Py_DEBUG' is unset, Python ABI tag may be incorrect
   warn=(impl == 'cp')):
 C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages\wheel\bdist_wheel.py:87: RuntimeWarning: Config variable 'WITH_PYMALLOC' is unset, Python ABI tag may be incorrect
   sys.version_info < (3, 8))) \
adding license file "LICENSE" (matched pattern "LICEN[CS]E*")
adding license file "AUTHORS" (matched pattern "AUTHORS*")
creating build\bdist.win32\wheel\Kivy-2.0.0.dist-info\WHEEL
creating 'dist\Kivy-2.0.0-cp36-cp36m-win32.whl' and adding 'build\bdist.win32\wheel' to it
adding 'Kivy-2.0.0.data/data/share/kivy-examples/3Drendering/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/3Drendering/monkey.obj'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/3Drendering/objloader.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/3Drendering/simple.glsl'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/RST_Editor/editor.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/RST_Editor/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/android/compass/android.txt'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/android/compass/compass.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/android/compass/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/android/compass/needle.png'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/android/compass/rose.png'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/android/takepicture/android.txt'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/android/takepicture/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/android/takepicture/shadow32.png'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/android/takepicture/takepicture.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/animation/animate.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/application/app_suite.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/application/app_with_build.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/application/app_with_config.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/application/app_with_kv.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/application/app_with_kv_in_template1.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/application/test.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/application/testkvfile.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/application/app_suite_data/testkvdir.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/application/template1/test.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/async/asyncio_advanced.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/async/asyncio_basic.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/async/trio_advanced.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/async/trio_basic.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/audio/12908_sweet_trip_mm_clap_hi.wav'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/audio/12909_sweet_trip_mm_clap_lo.wav'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/audio/12910_sweet_trip_mm_clap_mid.wav'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/audio/12911_sweet_trip_mm_hat_cl.wav'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/audio/12913_sweet_trip_mm_kick_hi.wav'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/audio/12914_sweet_trip_mm_kick_lo.wav'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/audio/12915_sweet_trip_mm_kick_mid.wav'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/audio/12916_sweet_trip_mm_kwik_mod_01.wav'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/audio/12917_sweet_trip_mm_kwik_mod_02.wav'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/audio/12918_sweet_trip_mm_kwik_mod_03.wav'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/audio/12919_sweet_trip_mm_kwik_mod_04.wav'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/audio/12920_sweet_trip_mm_kwik_mod_05.wav'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/audio/12921_sweet_trip_mm_kwik_mod_06.wav'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/audio/12922_sweet_trip_mm_kwik_mod_07.wav'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/audio/12923_sweet_trip_mm_metal_clave.wav'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/audio/12925_sweet_trip_mm_sweep_x.wav'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/audio/12926_sweet_trip_mm_sweep_y.wav'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/audio/12927_sweet_trip_mm_sweep_z.wav'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/audio/audio.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/audio/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/audio/pitch.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/camera/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/canvas/bezier.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/canvas/canvas_stress.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/canvas/circle.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/canvas/fbo_canvas.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/canvas/kiwi.jpg'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/canvas/lines.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/canvas/lines_extended.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/canvas/mesh.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/canvas/mesh_manipulation.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/canvas/mtexture1.png'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/canvas/mtexture2.png'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/canvas/multitexture.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/canvas/repeat_texture.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/canvas/rotation.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/canvas/rounded_rectangle.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/canvas/scale.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/canvas/stencil_canvas.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/canvas/tesselate.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/canvas/texture.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/canvas/texture_example_image.png'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/container/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/container/kv/1.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/container/kv/2.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/container/kv/3.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/container/kv/root.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/cover/cover_image.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/cover/cover_video.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/camera_puzzle.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/kivycatalog/kivycatalog.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/kivycatalog/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/kivycatalog/container_kvs/AnchorLayoutContainer.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/kivycatalog/container_kvs/BoxLayoutContainer.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/kivycatalog/container_kvs/ButtonContainer.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/kivycatalog/container_kvs/CheckBoxContainer.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/kivycatalog/container_kvs/FileChooserContainer.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/kivycatalog/container_kvs/FloatLayoutContainer.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/kivycatalog/container_kvs/GridLayoutContainer.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/kivycatalog/container_kvs/LabelContainer.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/kivycatalog/container_kvs/MediaContainer.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/kivycatalog/container_kvs/PlaygroundContainer.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/kivycatalog/container_kvs/PopupContainer.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/kivycatalog/container_kvs/ProgressBarContainer.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/kivycatalog/container_kvs/RestContainer.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/kivycatalog/container_kvs/ScatterContainer.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/kivycatalog/container_kvs/SelectorsContainer.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/kivycatalog/container_kvs/StackLayoutContainer.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/kivycatalog/container_kvs/TextContainer.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/multistroke/gesturedatabase.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/multistroke/gesturedatabase.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/multistroke/helpers.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/multistroke/historymanager.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/multistroke/historymanager.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/multistroke/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/multistroke/multistroke.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/multistroke/settings.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/multistroke/settings.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/pictures/android.txt'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/pictures/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/pictures/pictures.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/pictures/shadow32.png'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/pictures/images/Bubbles.jpg'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/pictures/images/Ill1.jpg'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/pictures/images/Wall.jpg'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/pictures/images/faust_github.jpg'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/shadereditor/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/shadereditor/shadereditor.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/README.txt'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/android.txt'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/showcase.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/background.png'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/faust_github.jpg'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/icons/README'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/icons/bug.png'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/icons/chevron-left.png'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/icons/chevron-right.png'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/screens/accordions.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/screens/bubbles.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/screens/buttons.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/screens/carousel.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/screens/checkboxes.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/screens/codeinput.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/screens/dropdown.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/screens/filechoosers.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/screens/popups.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/screens/progressbar.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/screens/rstdocument.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/screens/scatter.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/screens/screenmanager.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/screens/sliders.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/screens/spinner.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/screens/splitter.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/screens/switches.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/screens/tabbedpanel + layouts.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/screens/textinputs.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/showcase/data/screens/togglebutton.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/touchtracer/README.txt'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/touchtracer/android.txt'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/touchtracer/icon.png'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/touchtracer/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/touchtracer/particle.png'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/demo/touchtracer/touchtracer.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/frameworks/twisted/echo_client_app.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/frameworks/twisted/echo_server_app.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/frameworks/twisted/twistd_app.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/gestures/gesture_board.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/gestures/my_gestures.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/guide/designwithkv/controller.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/guide/designwithkv/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/guide/firstwidget/1_skeleton.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/guide/firstwidget/2_print_touch.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/guide/firstwidget/3_draw_ellipse.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/guide/firstwidget/4_draw_line.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/guide/firstwidget/5_random_colors.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/guide/firstwidget/6_button.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/guide/quickstart/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/includes/button.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/includes/layout.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/includes/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/includes/test.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/keyboard/android.txt'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/keyboard/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/keyboard/numeric.json'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/kinect/README.txt'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/kinect/kinectviewer.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/kv/app_button.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/kv/app_camera.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/kv/app_fbo.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/kv/app_layout.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/kv/app_logo.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/kv/app_scatter.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/kv/app_stencil.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/kv/app_video.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/kv/builder_template.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/kv/kivy.jpg'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/kv/kvrun.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/kv/ids/id_in_kv/id_in_kv.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/kv/ids/id_in_kv/test.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/kv/ids/kv_and_py/kv_and_py.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/kv/ids/kv_and_py/test.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/miscellaneous/clipboard.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/miscellaneous/imagesave.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/miscellaneous/joystick.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/miscellaneous/multiple_dropfile.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/miscellaneous/on_textedit_event.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/miscellaneous/shapecollisions.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/miscellaneous/shapedwindow.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/miscellaneous/two_panes.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/miscellaneous/urlrequest.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/settings/android.txt'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/settings/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/shader/plasma.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/shader/plasma.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/shader/rotated.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/shader/rotated.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/shader/shadertree.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/shader/shadertree.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/shader/tex3.jpg'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/svg/benchmark.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/svg/cloud.svg'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/svg/main-smaa.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/svg/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/svg/music.svg'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/svg/ship.svg'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/svg/sun.svg'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/svg/tiger.svg'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/text/pango_demo.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/tutorials/notes/final/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/tutorials/notes/final/note.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/tutorials/notes/final/data/icon.png'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/tutorials/pong/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/tutorials/pong/pong.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/tutorials/pong/steps/step1/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/tutorials/pong/steps/step1/pong.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/tutorials/pong/steps/step2/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/tutorials/pong/steps/step2/pong.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/tutorials/pong/steps/step3/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/tutorials/pong/steps/step3/pong.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/tutorials/pong/steps/step4/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/tutorials/pong/steps/step4/pong.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/tutorials/pong/steps/step5/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/tutorials/pong/steps/step5/pong.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/accordion_1.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/actionbar.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/asyncimage.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/boxlayout_poshint.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/bubble_test.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/camera.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/carousel_buttons.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/cityCC0.mpg'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/cityCC0.png'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/codeinput.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/codeinputtest.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/colorpicker.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/colorusage.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/compound_selection.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/customcollide.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/effectwidget.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/effectwidget2.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/effectwidget3_advanced.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/fbowidget.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/focus_behavior.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/image_mipmap.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/keyboardlistener.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/label_mipmap.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/label_sizing.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/label_text_size.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/label_with_markup.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/lang_dynamic_classes.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/pagelayout.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/popup_with_kv.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/rstexample.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/scatter.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/scatter.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/screenmanager.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/scrollview.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/scrollview.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/settings.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/shorten_text.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/spinner.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/splitter.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/tabbed_panel_showcase.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/tabbedpanel.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/textalign.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/textalign.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/textinput.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/unicode_textinput.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/videoplayer.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/recycleview/basic_data.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/recycleview/infinite_scrolling.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/recycleview/key_viewclass.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/recycleview/messenger.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/recycleview/pull_to_refresh.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/recycleview/rv_animate_items.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/sequenced_images/android.txt'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/sequenced_images/main.kv'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/sequenced_images/main.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/sequenced_images/data/images/bird.zip'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/sequenced_images/data/images/button_white.png'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/sequenced_images/data/images/button_white_animated.zip'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/sequenced_images/data/images/cube.zip'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/sequenced_images/data/images/info.png'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/sequenced_images/data/images/info.zip'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/sequenced_images/data/images/simple_cv_joint_animated.gif'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/sequenced_images/uix/__init__.py'
adding 'Kivy-2.0.0.data/data/share/kivy-examples/widgets/sequenced_images/uix/custom_button.py'
adding 'kivy/__init__.py'
adding 'kivy/_clock.cp36-win32.pdb'
adding 'kivy/_clock.cp36-win32.pyd'
adding 'kivy/_clock.pxd'
adding 'kivy/_event.cp36-win32.pdb'
adding 'kivy/_event.cp36-win32.pyd'
adding 'kivy/_event.pxd'
adding 'kivy/_version.py'
adding 'kivy/animation.py'
adding 'kivy/app.py'
adding 'kivy/atlas.py'
adding 'kivy/base.py'
adding 'kivy/cache.py'
adding 'kivy/clock.py'
adding 'kivy/compat.py'
adding 'kivy/config.py'
adding 'kivy/context.py'
adding 'kivy/event.py'
adding 'kivy/factory.py'
adding 'kivy/factory_registers.py'
adding 'kivy/geometry.py'
adding 'kivy/gesture.py'
adding 'kivy/interactive.py'
adding 'kivy/loader.py'
adding 'kivy/logger.py'
adding 'kivy/metrics.py'
adding 'kivy/multistroke.py'
adding 'kivy/parser.py'
adding 'kivy/properties.cp36-win32.pdb'
adding 'kivy/properties.cp36-win32.pyd'
adding 'kivy/properties.pxd'
adding 'kivy/resources.py'
adding 'kivy/setupconfig.py'
adding 'kivy/support.py'
adding 'kivy/utils.py'
adding 'kivy/vector.py'
adding 'kivy/weakmethod.py'
adding 'kivy/weakproxy.cp36-win32.pdb'
adding 'kivy/weakproxy.cp36-win32.pyd'
adding 'kivy/core/__init__.py'
adding 'kivy/core/audio/__init__.py'
adding 'kivy/core/audio/audio_android.py'
adding 'kivy/core/audio/audio_avplayer.py'
adding 'kivy/core/audio/audio_ffpyplayer.py'
adding 'kivy/core/audio/audio_gstplayer.py'
adding 'kivy/core/audio/audio_pygame.py'
adding 'kivy/core/audio/audio_sdl2.cp36-win32.pdb'
adding 'kivy/core/audio/audio_sdl2.cp36-win32.pyd'
adding 'kivy/core/camera/__init__.py'
adding 'kivy/core/camera/camera_android.py'
adding 'kivy/core/camera/camera_gi.py'
adding 'kivy/core/camera/camera_opencv.py'
adding 'kivy/core/camera/camera_picamera.py'
adding 'kivy/core/clipboard/__init__.py'
adding 'kivy/core/clipboard/_clipboard_ext.py'
adding 'kivy/core/clipboard/_clipboard_sdl2.cp36-win32.pdb'
adding 'kivy/core/clipboard/_clipboard_sdl2.cp36-win32.pyd'
adding 'kivy/core/clipboard/clipboard_android.py'
adding 'kivy/core/clipboard/clipboard_dbusklipper.py'
adding 'kivy/core/clipboard/clipboard_dummy.py'
adding 'kivy/core/clipboard/clipboard_gtk3.py'
adding 'kivy/core/clipboard/clipboard_nspaste.py'
adding 'kivy/core/clipboard/clipboard_pygame.py'
adding 'kivy/core/clipboard/clipboard_sdl2.py'
adding 'kivy/core/clipboard/clipboard_winctypes.py'
adding 'kivy/core/clipboard/clipboard_xclip.py'
adding 'kivy/core/clipboard/clipboard_xsel.py'
adding 'kivy/core/gl/__init__.py'
adding 'kivy/core/image/__init__.py'
adding 'kivy/core/image/_img_sdl2.cp36-win32.pdb'
adding 'kivy/core/image/_img_sdl2.cp36-win32.pyd'
adding 'kivy/core/image/img_dds.py'
adding 'kivy/core/image/img_ffpyplayer.py'
adding 'kivy/core/image/img_pil.py'
adding 'kivy/core/image/img_pygame.py'
adding 'kivy/core/image/img_sdl2.py'
adding 'kivy/core/image/img_tex.py'
adding 'kivy/core/spelling/__init__.py'
adding 'kivy/core/spelling/spelling_enchant.py'
adding 'kivy/core/spelling/spelling_osxappkit.py'
adding 'kivy/core/text/__init__.py'
adding 'kivy/core/text/_text_sdl2.cp36-win32.pdb'
adding 'kivy/core/text/_text_sdl2.cp36-win32.pyd'
adding 'kivy/core/text/markup.py'
adding 'kivy/core/text/text_layout.cp36-win32.pdb'
adding 'kivy/core/text/text_layout.cp36-win32.pyd'
adding 'kivy/core/text/text_layout.pxd'
adding 'kivy/core/text/text_pango.py'
adding 'kivy/core/text/text_pil.py'
adding 'kivy/core/text/text_pygame.py'
adding 'kivy/core/text/text_sdl2.py'
adding 'kivy/core/video/__init__.py'
adding 'kivy/core/video/video_ffmpeg.py'
adding 'kivy/core/video/video_ffpyplayer.py'
adding 'kivy/core/video/video_gstplayer.py'
adding 'kivy/core/video/video_null.py'
adding 'kivy/core/window/__init__.py'
adding 'kivy/core/window/_window_sdl2.cp36-win32.pdb'
adding 'kivy/core/window/_window_sdl2.cp36-win32.pyd'
adding 'kivy/core/window/window_attrs.pxi'
adding 'kivy/core/window/window_egl_rpi.py'
adding 'kivy/core/window/window_info.cp36-win32.pdb'
adding 'kivy/core/window/window_info.cp36-win32.pyd'
adding 'kivy/core/window/window_info.pxd'
adding 'kivy/core/window/window_pygame.py'
adding 'kivy/core/window/window_sdl2.py'
adding 'kivy/data/settings_kivy.json'
adding 'kivy/data/style.kv'
adding 'kivy/data/fonts/DejaVuSans.ttf'
adding 'kivy/data/fonts/Roboto-Bold.ttf'
adding 'kivy/data/fonts/Roboto-BoldItalic.ttf'
adding 'kivy/data/fonts/Roboto-Italic.ttf'
adding 'kivy/data/fonts/Roboto-Regular.ttf'
adding 'kivy/data/fonts/RobotoMono-Regular.ttf'
adding 'kivy/data/glsl/default.fs'
adding 'kivy/data/glsl/default.png'
adding 'kivy/data/glsl/default.vs'
adding 'kivy/data/glsl/header.fs'
adding 'kivy/data/glsl/header.vs'
adding 'kivy/data/images/background.jpg'
adding 'kivy/data/images/cursor.png'
adding 'kivy/data/images/defaultshape.png'
adding 'kivy/data/images/defaulttheme-0.png'
adding 'kivy/data/images/defaulttheme.atlas'
adding 'kivy/data/images/image-loading.gif'
adding 'kivy/data/images/image-loading.zip'
adding 'kivy/data/images/testpattern.png'
adding 'kivy/data/keyboards/azerty.json'
adding 'kivy/data/keyboards/de.json'
adding 'kivy/data/keyboards/de_CH.json'
adding 'kivy/data/keyboards/en_US.json'
adding 'kivy/data/keyboards/fr_CH.json'
adding 'kivy/data/keyboards/qwerty.json'
adding 'kivy/data/keyboards/qwertz.json'
adding 'kivy/data/logo/kivy-icon-128.png'
adding 'kivy/data/logo/kivy-icon-16.png'
adding 'kivy/data/logo/kivy-icon-24.png'
adding 'kivy/data/logo/kivy-icon-256.png'
adding 'kivy/data/logo/kivy-icon-32.png'
adding 'kivy/data/logo/kivy-icon-48.png'
adding 'kivy/data/logo/kivy-icon-512.png'
adding 'kivy/data/logo/kivy-icon-64.ico'
adding 'kivy/data/logo/kivy-icon-64.png'
adding 'kivy/deps/__init__.py'
adding 'kivy/effects/__init__.py'
adding 'kivy/effects/dampedscroll.py'
adding 'kivy/effects/kinetic.py'
adding 'kivy/effects/opacityscroll.py'
adding 'kivy/effects/scroll.py'
adding 'kivy/extras/__init__.py'
adding 'kivy/extras/highlight.py'
adding 'kivy/garden/__init__.py'
adding 'kivy/graphics/__init__.py'
adding 'kivy/graphics/buffer.cp36-win32.pdb'
adding 'kivy/graphics/buffer.cp36-win32.pyd'
adding 'kivy/graphics/buffer.pxd'
adding 'kivy/graphics/cgl.cp36-win32.pdb'
adding 'kivy/graphics/cgl.cp36-win32.pyd'
adding 'kivy/graphics/cgl.pxd'
adding 'kivy/graphics/common.pxi'
adding 'kivy/graphics/compiler.cp36-win32.pdb'
adding 'kivy/graphics/compiler.cp36-win32.pyd'
adding 'kivy/graphics/compiler.pxd'
adding 'kivy/graphics/context.cp36-win32.pdb'
adding 'kivy/graphics/context.cp36-win32.pyd'
adding 'kivy/graphics/context.pxd'
adding 'kivy/graphics/context_instructions.cp36-win32.pdb'
adding 'kivy/graphics/context_instructions.cp36-win32.pyd'
adding 'kivy/graphics/context_instructions.pxd'
adding 'kivy/graphics/fbo.cp36-win32.pdb'
adding 'kivy/graphics/fbo.cp36-win32.pyd'
adding 'kivy/graphics/fbo.pxd'
adding 'kivy/graphics/gl_debug_logger.pxi'
adding 'kivy/graphics/gl_instructions.cp36-win32.pdb'
adding 'kivy/graphics/gl_instructions.cp36-win32.pyd'
adding 'kivy/graphics/img_tools.pxi'
adding 'kivy/graphics/instructions.cp36-win32.pdb'
adding 'kivy/graphics/instructions.cp36-win32.pyd'
adding 'kivy/graphics/instructions.pxd'
adding 'kivy/graphics/memory.pxi'
adding 'kivy/graphics/opcodes.pxi'
adding 'kivy/graphics/opengl.cp36-win32.pdb'
adding 'kivy/graphics/opengl.cp36-win32.pyd'
adding 'kivy/graphics/opengl_utils.cp36-win32.pdb'
adding 'kivy/graphics/opengl_utils.cp36-win32.pyd'
adding 'kivy/graphics/opengl_utils.pxd'
adding 'kivy/graphics/opengl_utils_def.pxi'
adding 'kivy/graphics/scissor_instructions.cp36-win32.pdb'
adding 'kivy/graphics/scissor_instructions.cp36-win32.pyd'
adding 'kivy/graphics/shader.cp36-win32.pdb'
adding 'kivy/graphics/shader.cp36-win32.pyd'
adding 'kivy/graphics/shader.pxd'
adding 'kivy/graphics/stencil_instructions.cp36-win32.pdb'
adding 'kivy/graphics/stencil_instructions.cp36-win32.pyd'
adding 'kivy/graphics/stencil_instructions.pxd'
adding 'kivy/graphics/svg.cp36-win32.pdb'
adding 'kivy/graphics/svg.cp36-win32.pyd'
adding 'kivy/graphics/svg.pxd'
adding 'kivy/graphics/tesselator.cp36-win32.pdb'
adding 'kivy/graphics/tesselator.cp36-win32.pyd'
adding 'kivy/graphics/tesselator.pxd'
adding 'kivy/graphics/texture.cp36-win32.pdb'
adding 'kivy/graphics/texture.cp36-win32.pyd'
adding 'kivy/graphics/texture.pxd'
adding 'kivy/graphics/transformation.cp36-win32.pdb'
adding 'kivy/graphics/transformation.cp36-win32.pyd'
adding 'kivy/graphics/transformation.pxd'
adding 'kivy/graphics/vbo.cp36-win32.pdb'
adding 'kivy/graphics/vbo.cp36-win32.pyd'
adding 'kivy/graphics/vbo.pxd'
adding 'kivy/graphics/vertex.cp36-win32.pdb'
adding 'kivy/graphics/vertex.cp36-win32.pyd'
adding 'kivy/graphics/vertex.pxd'
adding 'kivy/graphics/vertex_instructions.cp36-win32.pdb'
adding 'kivy/graphics/vertex_instructions.cp36-win32.pyd'
adding 'kivy/graphics/vertex_instructions.pxd'
adding 'kivy/graphics/vertex_instructions_line.pxi'
adding 'kivy/graphics/cgl_backend/__init__.py'
adding 'kivy/graphics/cgl_backend/cgl_debug.cp36-win32.pdb'
adding 'kivy/graphics/cgl_backend/cgl_debug.cp36-win32.pyd'
adding 'kivy/graphics/cgl_backend/cgl_gl.cp36-win32.pdb'
adding 'kivy/graphics/cgl_backend/cgl_gl.cp36-win32.pyd'
adding 'kivy/graphics/cgl_backend/cgl_glew.cp36-win32.pdb'
adding 'kivy/graphics/cgl_backend/cgl_glew.cp36-win32.pyd'
adding 'kivy/graphics/cgl_backend/cgl_mock.cp36-win32.pdb'
adding 'kivy/graphics/cgl_backend/cgl_mock.cp36-win32.pyd'
adding 'kivy/graphics/cgl_backend/cgl_sdl2.cp36-win32.pdb'
adding 'kivy/graphics/cgl_backend/cgl_sdl2.cp36-win32.pyd'
adding 'kivy/include/common_subset.h'
adding 'kivy/include/config.h'
adding 'kivy/include/config.pxi'
adding 'kivy/include/gl2platform.h'
adding 'kivy/include/gl_redirect.h'
adding 'kivy/include/khrplatform.h'
adding 'kivy/input/__init__.py'
adding 'kivy/input/factory.py'
adding 'kivy/input/motionevent.py'
adding 'kivy/input/provider.py'
adding 'kivy/input/recorder.py'
adding 'kivy/input/shape.py'
adding 'kivy/input/postproc/__init__.py'
adding 'kivy/input/postproc/calibration.py'
adding 'kivy/input/postproc/dejitter.py'
adding 'kivy/input/postproc/doubletap.py'
adding 'kivy/input/postproc/ignorelist.py'
adding 'kivy/input/postproc/retaintouch.py'
adding 'kivy/input/postproc/tripletap.py'
adding 'kivy/input/providers/__init__.py'
adding 'kivy/input/providers/androidjoystick.py'
adding 'kivy/input/providers/hidinput.py'
adding 'kivy/input/providers/leapfinger.py'
adding 'kivy/input/providers/linuxwacom.py'
adding 'kivy/input/providers/mactouch.py'
adding 'kivy/input/providers/mouse.py'
adding 'kivy/input/providers/mtdev.py'
adding 'kivy/input/providers/probesysfs.py'
adding 'kivy/input/providers/tuio.py'
adding 'kivy/input/providers/wm_common.py'
adding 'kivy/input/providers/wm_pen.py'
adding 'kivy/input/providers/wm_touch.py'
adding 'kivy/lang/__init__.py'
adding 'kivy/lang/builder.py'
adding 'kivy/lang/parser.py'
adding 'kivy/lib/__init__.py'
adding 'kivy/lib/ddsfile.py'
adding 'kivy/lib/mtdev.py'
adding 'kivy/lib/sdl2.pxi'
adding 'kivy/lib/gstplayer/__init__.py'
adding 'kivy/lib/pango/pangoft2.pxi'
adding 'kivy/lib/vidcore_lite/__init__.py'
adding 'kivy/lib/vidcore_lite/bcm.pxd'
adding 'kivy/modules/__init__.py'
adding 'kivy/modules/_webdebugger.py'
adding 'kivy/modules/console.py'
adding 'kivy/modules/cursor.py'
adding 'kivy/modules/inspector.py'
adding 'kivy/modules/joycursor.py'
adding 'kivy/modules/keybinding.py'
adding 'kivy/modules/monitor.py'
adding 'kivy/modules/recorder.py'
adding 'kivy/modules/screen.py'
adding 'kivy/modules/showborder.py'
adding 'kivy/modules/touchring.py'
adding 'kivy/modules/webdebugger.py'
adding 'kivy/network/__init__.py'
adding 'kivy/network/urlrequest.py'
adding 'kivy/storage/__init__.py'
adding 'kivy/storage/dictstore.py'
adding 'kivy/storage/jsonstore.py'
adding 'kivy/storage/redisstore.py'
adding 'kivy/tests/__init__.py'
adding 'kivy/tests/async_common.py'
adding 'kivy/tests/common.py'
adding 'kivy/tests/conftest.py'
adding 'kivy/tests/coverage_lang.kv'
adding 'kivy/tests/fixtures.py'
adding 'kivy/tests/perf_test_textinput.py'
adding 'kivy/tests/sample1.ogg'
adding 'kivy/tests/test_animations.py'
adding 'kivy/tests/test_app.py'
adding 'kivy/tests/test_audio.py'
adding 'kivy/tests/test_button.png'
adding 'kivy/tests/test_clipboard.py'
adding 'kivy/tests/test_clock.py'
adding 'kivy/tests/test_coverage.py'
adding 'kivy/tests/test_doc_gallery.py'
adding 'kivy/tests/test_fbo_py2py3.py'
adding 'kivy/tests/test_filechooser.py'
adding 'kivy/tests/test_filechooser_unicode.py'
adding 'kivy/tests/test_fonts.py'
adding 'kivy/tests/test_graphics.py'
adding 'kivy/tests/test_image.py'
adding 'kivy/tests/test_imageloader.py'
adding 'kivy/tests/test_invalid_lang.py'
adding 'kivy/tests/test_knspace.py'
adding 'kivy/tests/test_lang.py'
adding 'kivy/tests/test_lang_complex.py'
adding 'kivy/tests/test_lang_pre_process_and_post_process.py'
adding 'kivy/tests/test_module_inspector.py'
adding 'kivy/tests/test_mouse_multitouchsim.py'
adding 'kivy/tests/test_multistroke.py'
adding 'kivy/tests/test_properties.py'
adding 'kivy/tests/test_rst_replace.py'
adding 'kivy/tests/test_screen.py'
adding 'kivy/tests/test_storage.py'
adding 'kivy/tests/test_uix_actionbar.py'
adding 'kivy/tests/test_uix_anchorlayout.py'
adding 'kivy/tests/test_uix_asyncimage.py'
adding 'kivy/tests/test_uix_boxlayout.py'
adding 'kivy/tests/test_uix_bubble.py'
adding 'kivy/tests/test_uix_carousel.py'
adding 'kivy/tests/test_uix_dropdown.py'
adding 'kivy/tests/test_uix_gridlayout.py'
adding 'kivy/tests/test_uix_layout.py'
adding 'kivy/tests/test_uix_modal.py'
adding 'kivy/tests/test_uix_relativelayout.py'
adding 'kivy/tests/test_uix_scrollview.py'
adding 'kivy/tests/test_uix_slider.py'
adding 'kivy/tests/test_uix_stacklayout.py'
adding 'kivy/tests/test_uix_textinput.py'
adding 'kivy/tests/test_uix_translate_coordinates.py'
adding 'kivy/tests/test_uix_widget.py'
adding 'kivy/tests/test_urlrequest.py'
adding 'kivy/tests/test_utils.py'
adding 'kivy/tests/test_vector.py'
adding 'kivy/tests/test_video.py'
adding 'kivy/tests/test_weakmethod.py'
adding 'kivy/tests/test_widget.py'
adding 'kivy/tests/test_widget_walk.py'
adding 'kivy/tests/test_window_info.py'
adding 'kivy/tests/testkv.kv'
adding 'kivy/tests/unicode_files.zip'
adding 'kivy/tests/unicode_font.zip'
adding 'kivy/tests/visual_test_label.py'
adding 'kivy/tests/pyinstaller/test_pyinstaller.py'
adding 'kivy/tests/pyinstaller/simple_widget/main.py'
adding 'kivy/tests/pyinstaller/simple_widget/main.spec'
adding 'kivy/tests/pyinstaller/simple_widget/project/__init__.py'
adding 'kivy/tests/pyinstaller/simple_widget/project/widget.py'
adding 'kivy/tests/pyinstaller/video_widget/main.py'
adding 'kivy/tests/pyinstaller/video_widget/main.spec'
adding 'kivy/tests/pyinstaller/video_widget/project/__init__.py'
adding 'kivy/tests/test_issues/test_6315.py'
adding 'kivy/tests/test_issues/test_issue_1084.py'
adding 'kivy/tests/test_issues/test_issue_1091.py'
adding 'kivy/tests/test_issues/test_issue_599.py'
adding 'kivy/tests/test_issues/test_issue_609.py'
adding 'kivy/tests/test_issues/test_issue_6909.py'
adding 'kivy/tests/test_issues/test_issue_883.py'
adding 'kivy/tools/__init__.py'
adding 'kivy/tools/benchmark.py'
adding 'kivy/tools/changelog_parser.py'
adding 'kivy/tools/coverage.py'
adding 'kivy/tools/gallery.py'
adding 'kivy/tools/generate-icons.py'
adding 'kivy/tools/kviewer.py'
adding 'kivy/tools/report.py'
adding 'kivy/tools/stub-gl-debug.py'
adding 'kivy/tools/texturecompress.py'
adding 'kivy/tools/gles_compat/gl2.h'
adding 'kivy/tools/gles_compat/subset_gles.py'
adding 'kivy/tools/highlight/__init__.py'
adding 'kivy/tools/highlight/kivy-mode.el'
adding 'kivy/tools/highlight/kivy.json-tmlanguage'
adding 'kivy/tools/highlight/kivy.tmLanguage'
adding 'kivy/tools/highlight/kivy.vim'
adding 'kivy/tools/image-testsuite/README.md'
adding 'kivy/tools/image-testsuite/gimp28-testsuite.py'
adding 'kivy/tools/image-testsuite/imagemagick-testsuite.sh'
adding 'kivy/tools/packaging/__init__.py'
adding 'kivy/tools/packaging/cython_cfg.py'
adding 'kivy/tools/packaging/factory.py'
adding 'kivy/tools/packaging/pyinstaller_hooks/__init__.py'
adding 'kivy/tools/packaging/pyinstaller_hooks/__main__.py'
adding 'kivy/tools/packaging/pyinstaller_hooks/hook-kivy.py'
adding 'kivy/tools/packaging/pyinstaller_hooks/pyi_rth_kivy.py'
adding 'kivy/tools/pep8checker/pep8.py'
adding 'kivy/tools/pep8checker/pep8kivy.py'
adding 'kivy/tools/pep8checker/pre-commit.githook'
adding 'kivy/tools/theming/defaulttheme/action_bar.png'
adding 'kivy/tools/theming/defaulttheme/action_group.png'
adding 'kivy/tools/theming/defaulttheme/action_group_disabled.png'
adding 'kivy/tools/theming/defaulttheme/action_group_down.png'
adding 'kivy/tools/theming/defaulttheme/action_item.png'
adding 'kivy/tools/theming/defaulttheme/action_item_down.png'
adding 'kivy/tools/theming/defaulttheme/action_view.png'
adding 'kivy/tools/theming/defaulttheme/audio-volume-high.png'
adding 'kivy/tools/theming/defaulttheme/audio-volume-low.png'
adding 'kivy/tools/theming/defaulttheme/audio-volume-medium.png'
adding 'kivy/tools/theming/defaulttheme/audio-volume-muted.png'
adding 'kivy/tools/theming/defaulttheme/bubble.png'
adding 'kivy/tools/theming/defaulttheme/bubble_arrow.png'
adding 'kivy/tools/theming/defaulttheme/bubble_btn.png'
adding 'kivy/tools/theming/defaulttheme/bubble_btn_pressed.png'
adding 'kivy/tools/theming/defaulttheme/button.png'
adding 'kivy/tools/theming/defaulttheme/button_disabled.png'
adding 'kivy/tools/theming/defaulttheme/button_disabled_pressed.png'
adding 'kivy/tools/theming/defaulttheme/button_pressed.png'
adding 'kivy/tools/theming/defaulttheme/checkbox_disabled_off.png'
adding 'kivy/tools/theming/defaulttheme/checkbox_disabled_on.png'
adding 'kivy/tools/theming/defaulttheme/checkbox_off.png'
adding 'kivy/tools/theming/defaulttheme/checkbox_on.png'
adding 'kivy/tools/theming/defaulttheme/checkbox_radio_disabled_off.png'
adding 'kivy/tools/theming/defaulttheme/checkbox_radio_disabled_on.png'
adding 'kivy/tools/theming/defaulttheme/checkbox_radio_off.png'
adding 'kivy/tools/theming/defaulttheme/checkbox_radio_on.png'
adding 'kivy/tools/theming/defaulttheme/close.png'
adding 'kivy/tools/theming/defaulttheme/filechooser_file.png'
adding 'kivy/tools/theming/defaulttheme/filechooser_folder.png'
adding 'kivy/tools/theming/defaulttheme/filechooser_selected.png'
adding 'kivy/tools/theming/defaulttheme/image-missing.png'
adding 'kivy/tools/theming/defaulttheme/media-playback-pause.png'
adding 'kivy/tools/theming/defaulttheme/media-playback-start.png'
adding 'kivy/tools/theming/defaulttheme/media-playback-stop.png'
adding 'kivy/tools/theming/defaulttheme/modalview-background.png'
adding 'kivy/tools/theming/defaulttheme/overflow.png'
adding 'kivy/tools/theming/defaulttheme/player-background.png'
adding 'kivy/tools/theming/defaulttheme/player-play-overlay.png'
adding 'kivy/tools/theming/defaulttheme/previous_normal.png'
adding 'kivy/tools/theming/defaulttheme/progressbar.png'
adding 'kivy/tools/theming/defaulttheme/progressbar_background.png'
adding 'kivy/tools/theming/defaulttheme/ring.png'
adding 'kivy/tools/theming/defaulttheme/selector_left.png'
adding 'kivy/tools/theming/defaulttheme/selector_middle.png'
adding 'kivy/tools/theming/defaulttheme/selector_right.png'
adding 'kivy/tools/theming/defaulttheme/separator.png'
adding 'kivy/tools/theming/defaulttheme/slider_cursor.png'
adding 'kivy/tools/theming/defaulttheme/slider_cursor_disabled.png'
adding 'kivy/tools/theming/defaulttheme/sliderh_background.png'
adding 'kivy/tools/theming/defaulttheme/sliderh_background_disabled.png'
adding 'kivy/tools/theming/defaulttheme/sliderv_background.png'
adding 'kivy/tools/theming/defaulttheme/sliderv_background_disabled.png'
adding 'kivy/tools/theming/defaulttheme/spinner.png'
adding 'kivy/tools/theming/defaulttheme/spinner_disabled.png'
adding 'kivy/tools/theming/defaulttheme/spinner_pressed.png'
adding 'kivy/tools/theming/defaulttheme/splitter.png'
adding 'kivy/tools/theming/defaulttheme/splitter_disabled.png'
adding 'kivy/tools/theming/defaulttheme/splitter_disabled_down.png'
adding 'kivy/tools/theming/defaulttheme/splitter_disabled_down_h.png'
adding 'kivy/tools/theming/defaulttheme/splitter_disabled_h.png'
adding 'kivy/tools/theming/defaulttheme/splitter_down.png'
adding 'kivy/tools/theming/defaulttheme/splitter_down_h.png'
adding 'kivy/tools/theming/defaulttheme/splitter_grip.png'
adding 'kivy/tools/theming/defaulttheme/splitter_grip_h.png'
adding 'kivy/tools/theming/defaulttheme/splitter_h.png'
adding 'kivy/tools/theming/defaulttheme/switch-background.png'
adding 'kivy/tools/theming/defaulttheme/switch-background_disabled.png'
adding 'kivy/tools/theming/defaulttheme/switch-button.png'
adding 'kivy/tools/theming/defaulttheme/switch-button_disabled.png'
adding 'kivy/tools/theming/defaulttheme/tab.png'
adding 'kivy/tools/theming/defaulttheme/tab_btn.png'
adding 'kivy/tools/theming/defaulttheme/tab_btn_disabled.png'
adding 'kivy/tools/theming/defaulttheme/tab_btn_disabled_pressed.png'
adding 'kivy/tools/theming/defaulttheme/tab_btn_pressed.png'
adding 'kivy/tools/theming/defaulttheme/tab_disabled.png'
adding 'kivy/tools/theming/defaulttheme/textinput.png'
adding 'kivy/tools/theming/defaulttheme/textinput_active.png'
adding 'kivy/tools/theming/defaulttheme/textinput_disabled.png'
adding 'kivy/tools/theming/defaulttheme/textinput_disabled_active.png'
adding 'kivy/tools/theming/defaulttheme/tree_closed.png'
adding 'kivy/tools/theming/defaulttheme/tree_opened.png'
adding 'kivy/tools/theming/defaulttheme/vkeyboard_background.png'
adding 'kivy/tools/theming/defaulttheme/vkeyboard_disabled_background.png'
adding 'kivy/tools/theming/defaulttheme/vkeyboard_disabled_key_down.png'
adding 'kivy/tools/theming/defaulttheme/vkeyboard_disabled_key_normal.png'
adding 'kivy/tools/theming/defaulttheme/vkeyboard_key_down.png'
adding 'kivy/tools/theming/defaulttheme/vkeyboard_key_normal.png'
adding 'kivy/uix/__init__.py'
adding 'kivy/uix/accordion.py'
adding 'kivy/uix/actionbar.py'
adding 'kivy/uix/anchorlayout.py'
adding 'kivy/uix/boxlayout.py'
adding 'kivy/uix/bubble.py'
adding 'kivy/uix/button.py'
adding 'kivy/uix/camera.py'
adding 'kivy/uix/carousel.py'
adding 'kivy/uix/checkbox.py'
adding 'kivy/uix/codeinput.py'
adding 'kivy/uix/colorpicker.py'
adding 'kivy/uix/dropdown.py'
adding 'kivy/uix/effectwidget.py'
adding 'kivy/uix/filechooser.py'
adding 'kivy/uix/floatlayout.py'
adding 'kivy/uix/gesturesurface.py'
adding 'kivy/uix/gridlayout.py'
adding 'kivy/uix/image.py'
adding 'kivy/uix/label.py'
adding 'kivy/uix/layout.py'
adding 'kivy/uix/modalview.py'
adding 'kivy/uix/pagelayout.py'
adding 'kivy/uix/popup.py'
adding 'kivy/uix/progressbar.py'
adding 'kivy/uix/recycleboxlayout.py'
adding 'kivy/uix/recyclegridlayout.py'
adding 'kivy/uix/recyclelayout.py'
adding 'kivy/uix/relativelayout.py'
adding 'kivy/uix/rst.py'
adding 'kivy/uix/sandbox.py'
adding 'kivy/uix/scatter.py'
adding 'kivy/uix/scatterlayout.py'
adding 'kivy/uix/screenmanager.py'
adding 'kivy/uix/scrollview.py'
adding 'kivy/uix/settings.py'
adding 'kivy/uix/slider.py'
adding 'kivy/uix/spinner.py'
adding 'kivy/uix/splitter.py'
adding 'kivy/uix/stacklayout.py'
adding 'kivy/uix/stencilview.py'
adding 'kivy/uix/switch.py'
adding 'kivy/uix/tabbedpanel.py'
adding 'kivy/uix/textinput.py'
adding 'kivy/uix/togglebutton.py'
adding 'kivy/uix/treeview.py'
adding 'kivy/uix/video.py'
adding 'kivy/uix/videoplayer.py'
adding 'kivy/uix/vkeyboard.py'
adding 'kivy/uix/widget.py'
adding 'kivy/uix/behaviors/__init__.py'
adding 'kivy/uix/behaviors/button.py'
adding 'kivy/uix/behaviors/codenavigation.py'
adding 'kivy/uix/behaviors/compoundselection.py'
adding 'kivy/uix/behaviors/cover.py'
adding 'kivy/uix/behaviors/drag.py'
adding 'kivy/uix/behaviors/emacs.py'
adding 'kivy/uix/behaviors/focus.py'
adding 'kivy/uix/behaviors/knspace.py'
adding 'kivy/uix/behaviors/togglebutton.py'
adding 'kivy/uix/behaviors/touchripple.py'
adding 'kivy/uix/recycleview/__init__.py'
adding 'kivy/uix/recycleview/datamodel.py'
adding 'kivy/uix/recycleview/layout.py'
adding 'kivy/uix/recycleview/views.py'
adding 'Kivy-2.0.0.dist-info/AUTHORS'
adding 'Kivy-2.0.0.dist-info/LICENSE'
adding 'Kivy-2.0.0.dist-info/METADATA'
adding 'Kivy-2.0.0.dist-info/WHEEL'
adding 'Kivy-2.0.0.dist-info/dependency_links.txt'
adding 'Kivy-2.0.0.dist-info/top_level.txt'
adding 'Kivy-2.0.0.dist-info/RECORD'
removing build\bdist.win32\wheel
```



#### 4. 依赖库编译
Kivy 的依赖库SDL
SDL 主库
[SDL Release 2.0.12](https://github.com/libsdl-org/SDL/releases/tag/release-2.0.12)

SDL 字体库
[SDL_ttf  Release 2.0.15 ](https://github.com/libsdl-org/SDL_ttf/releases/tag/release-2.0.15) 

SDL 图片库
[SDL_image  Release 2.0.5 ](https://github.com/libsdl-org/SDL_image/releases/tag/release-2.0.5)


SDL 音频库
[SDL_mixer Release 2.0.4 ](https://github.com/libsdl-org/SDL_mixer/releases/tag/release-2.0.4)


GLEG 库
OpenGL 的扩展库， 实现跨平台支持和老版本的兼容 [GLEW Release 2.2.0](https://github.com/nigels-com/glew/releases/tag/glew-2.2.0)




编译报错
```log
\Kivy-2.0.0\kivy\core\clipboard\_clipboard_sdl2.c: fatal error C1041: cannot open program database 'D:\workspace\Kivy-2.0.0\vc140.pdb'; if multiple CL.EXE write to the same .PDB file, please use /FS


```
需要把生成的`vc140.pdb` 删除



加载kivy.clock 模块崩溃, 测试命令`python -X faulthandler -c "import kivy.clock"`
```shell
>python -X faulthandler -c "import kivy.clock"
sdl2 path:['C:\\Users\\guanglin.liang\\pythonEnv\\withPdbInfo\\share\\sdl2\\bin']
[INFO   ] [Logger      ] Record log in C:\Users\guanglin.liang\.kivy\logs\kivy_22-06-01_51.txt
[INFO   ] [deps        ] Successfully imported "kivy_deps.angle" 0.3.0
[INFO   ] [deps        ] Successfully imported "kivy_deps.glew" 0.3.0
[INFO   ] [deps        ] Successfully imported "kivy_deps.sdl2" 0.3.1
[INFO   ] [deps        ] Successfully imported "kivy_deps.sdl2_dev" 0.4.3
[INFO   ] [Kivy        ] v2.0.0
[INFO   ] [Kivy        ] Installed at "C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages\kivy-2.0.0-py3.6-win32.egg\kivy\__init__.py"
[INFO   ] [Python      ] v3.6.6 (v3.6.6:4cf1f54eb7, Jun 27 2018, 02:47:15) [MSC v.1900 32 bit (Intel)]
[INFO   ] [Python      ] Interpreter at "C:\Users\guanglin.liang\pythonEnv\withPdbInfo\Scripts\python.exe"
Windows fatal exception: access violation

Current thread 0x00001060 (most recent call first):
  File "<frozen importlib._bootstrap>", line 219 in _call_with_frames_removed
  File "<frozen importlib._bootstrap_external>", line 922 in create_module
  File "<frozen importlib._bootstrap>", line 571 in module_from_spec
  File "<frozen importlib._bootstrap>", line 658 in _load_unlocked
  File "<frozen importlib._bootstrap>", line 955 in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 971 in _find_and_load
  File "C:\Users\guanglin.liang\pythonEnv\withPdbInfo\lib\site-packages\kivy-2.0.0-py3.6-win32.egg\kivy\clock.py", line 466 in <module>
  File "<frozen importlib._bootstrap>", line 219 in _call_with_frames_removed
  File "<frozen importlib._bootstrap_external>", line 678 in exec_module
  File "<frozen importlib._bootstrap>", line 665 in _load_unlocked
  File "<frozen importlib._bootstrap>", line 955 in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 971 in _find_and_load
  File "<string>", line 1 in <module>


```

Release 和Debug 的exe 或者dll 互相调用会导致崩溃，比如优化选项、调试线程、链接runtime等库的问题


[VC 编译器`_DEBUG`选项定义问题](https://zhuanlan.zhihu.com/p/149865653)
[VC Release和Debug 区别](https://www.cnblogs.com/wangshenhe/archive/2012/05/16/2503943.html)
[Visual Studio C++编译选项](https://docs.microsoft.com/zh-cn/cpp/build/reference/debug-generate-debug-info?view=msvc-170)
[调试实战 —— dll 加载失败之 Debug Release 争锋篇](https://bianchengnan.gitee.io/articles/debugging-dll-load-failure-caused-by-mixed-configuration/)