# 良友影视质量优选规则 · MediaProfiles

[← 返回良友资源中心](https://maddestalistar.github.io/LiangYou-ResourceHub/) · v0.1 · 2026-10-23

把经常讨论的 **4K / UHD REMUX / Blu-ray / WEB-DL / DV / HDR10 / Atmos / TrueHD / DTS-HD MA / HEVC** 转为可读的**片源候选评分参考**。

## 三套独立偏好方案

| 文件 | 定位 | 示例 |
| --- | --- | --- |
| [均衡 4K](profiles/balanced-4k.json) | 兼顾画质、带宽与音轨 | 多数家庭播放器 |
| [容量优先](profiles/storage-saver.json) | 优先控制空间与文件体积 | NAS 小容量盘 |
| [原盘优先](profiles/remux-first.json) | UHD REMUX > 其他同类格式 | 高码率直连 |

## 快速试用

需要 Python 3，无外部依赖：

```bash
python3 scripts/score_releases.py --profile balanced-4k
python3 scripts/score_releases.py --profile storage-saver
python3 scripts/score_releases.py --profile remux-first
python3 -m unittest discover -s tests
```

可以把自己的候选文件名和大小填入 `examples/releases.json`；工具会打印得分、匹配依据、排序。相同电影/剧集的不同版本建议单独对比。

**兼容说明（重要）**：仓库的 `profiles/*.json` 是 **良友自有格式的可编辑参考规则**，**不是** Radarr / Sonarr 可直接导入的 Quality Profile JSON，也不会自动改变下载设置。Radarr/Sonarr 使用 Custom Formats 和 Quality Profiles，需按各自版本的界面将偏好分项转换并验证。Sonarr v4+、Radarr 的结构与评分策略也可能不同。本库当前只提供本地离线评分器，不假装已支持直接导入。参阅 [TRaSH Guides 自定义格式导入说明](https://trash-guides.info/Sonarr/sonarr-import-custom-formats/)。

## 已知边界

- 用文件名做正则判断，无法验证真实媒体流；错误或模糊的标题可能误识别。
- 简化模型只用于同源候选优选建议，片源来源、编码参数、HDR 支持、语言字幕及个人空间预算同样关键。
- `maxGB` 在“容量优先”方案中仅作为示例阈值，需结合每个电影片长手动调整。
- 此规则不下载内容、不附带版权资源或资源站链接。
