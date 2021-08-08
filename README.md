# douyin

> 代码实现视频剪辑。。。(没必要搞了，不是自创的都会被检测到的，处分花时间自己讲解)

### liu_jin_sui_yue

流金岁月的脚本。比较乱，后面也不跑了，就不整理了。。。

- [face_recognition](https://github.com/ageitgey/face_recognition) 人脸识别，实现识别 **刘诗诗**
- ffmpeg 剪辑并合并片段

最终效果图

![](https://beef-1256523277.cos.ap-chengdu.myqcloud.com/uPic/gCjiLq.png)

单个效果图

![](https://beef-1256523277.cos.ap-chengdu.myqcloud.com/uPic/Dq619l.png)

总体来说还是不错的，但是判定为搬运。。。后面就不跑了

### cheng_you_qing

```shell
python3 ./cheng_you_qing/main_process.py
```

电视剧 《我可能不会爱你》

- 获取背景图片

来自剪映缓存文件（用用剪映就知道说的是什么了）

```
➜  202107312102 pwd
/Users/beer/Movies/JianyingPro/User Data/Projects/com.lveditor.draft/202107312102
➜  202107312102 cat draft_info.json  | jq .materials.canvases
[
  {
    "album_image": "",
    "blur": 0,
    "color": "",
    "id": "3404A197-7427-4224-9CD6-E4285D0F291C",
    "image": "/Users/beer/Library/Containers/com.lemon.lvpro/Data/Movies/JianyingPro/User Data/Cache/onlineMaterial/ecfdbb3913490a88402f2b6347705f59.png",
    "image_id": "",
    "image_name": "",
    "type": "canvas_image"
  }
]
```

然后 运行  **cut_image.py** 剪裁图片

````python
# -*- coding: UTF-8 -*-
from PIL import Image

"""
剪切为指定像素
"""


def main():
    img = Image.open("./lover.png")  # 1200 * 1200
    cropped = img.crop((262.5, 0, 262.5 + 675.0, 1200))  # (left, upper, right, lower)
    cropped.save("./bg.png")


if __name__ == '__main__':
    main()
````

- How do i put the image behind video by using FFmpeg?

中文搜索许久，没找到满意结果，换成英文第一个就是。。。。

[How do i put the image behind video by using FFmpeg?](https://video.stackexchange.com/questions/16975/how-do-i-put-the-image-behind-video-by-using-ffmpeg)

```shell
# 添加背景图片和标题
ffmpeg -loop 1 -i bg.png -i input.mp4 -filter_complex "[1:v]scale=1080:-1[fg];[0:v][fg]overlay=(W-w)/2:(H-h)/2:shortest=1,drawtext=text='xxxx':fontfile=kai.ttf:x=(w-text_w)/2:y=130:fontsize=60:fontcolor=red" -y result.mp4
```

- 剪切视频

```shell
# start:end 单位 s
MP4Box -splitx 10:15 1.mp4
MP4Box -splitz 10:15 1.mp4

# 主要 splitx splitz 区别，我没看懂，splitx 就丢失音频
```

结果：

![](https://beef-1256523277.cos.ap-chengdu.myqcloud.com/uPic/aZZbfq.png)

