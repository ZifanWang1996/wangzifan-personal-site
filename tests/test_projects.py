from pathlib import Path


SITE = Path(__file__).parents[1] / "index.html"


def test_projects_section_includes_live_palworldmap_v2_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>PalworldMap</h3>' in html
    assert 'href="https://palworldmap.best/"' in html
    assert '<span>04 · 已上线</span><span>Palworld 坐标图谱</span>' in html
    assert '89 条来源锁定导航记录（82 个快速传送点、7 座高塔）' in html
    assert '最近点计算与本地清单' in html


def test_projects_section_includes_live_codexskin_card():
    html = SITE.read_text(encoding="utf-8")

    assert 'data-status="live"' in html
    assert '<h3>CodexSkin.space</h3>' in html
    assert 'href="https://codexskin.space/"' in html
    assert '<span>05 · 已上线</span><span>Codex CLI TUI 指南站</span>' in html
    assert 'Codex CLI TUI 配置指南' in html


def test_projects_section_includes_live_llmstxt_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>llmstxt</h3>' in html
    assert 'href="https://llmstxt.best/"' in html
    assert '<span>06 · 已上线</span><span>llms.txt 实用指南</span>' in html
    assert 'llms.txt 的阅读、发布与维护' in html


def test_projects_section_includes_live_allwishescometrue_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>All Wishes Come True</h3>' in html
    assert 'href="https://allwishescometrue.site/"' in html
    assert '<span>07 · 已上线</span><span>八仙电影与民俗文化站</span>' in html
    assert '电影背景、八位角色、民俗源流' in html


def test_projects_section_includes_live_taskbarherowiki_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>TaskbarHeroWiki</h3>' in html
    assert 'href="https://taskbarherowiki.best/"' in html
    assert '<span>08 · 已上线</span><span>Task Bar Hero 数据库</span>' in html
    assert '关卡、怪物、宝箱、材料与关系记录' in html


def test_projects_section_includes_live_chinesecashcoins_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>Chinese Coins Atlas</h3>' in html
    assert 'href="https://chinesecashcoins.wiki/"' in html
    assert '<span>09 · 已上线</span><span>中国古钱币图鉴</span>' in html
    assert '布币、刀币、五铢、开元通宝' in html


def test_projects_section_includes_live_rotcheck_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>Rot Check</h3>' in html
    assert 'href="https://rotcheck.cyou/"' in html
    assert '<span>10 · 已上线</span><span>Gen Alpha 趣味测试站</span>' in html
    assert 'Am I Unc、Brainrot Test、Am I Cooked' in html


def test_projects_section_includes_live_spiritvale_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>SpiritVale Wiki</h3>' in html
    assert 'href="https://spiritvale.blog/"' in html
    assert '<span>11 · 已上线</span><span>SpiritVale 社区 Wiki</span>' in html
    assert '16 个职业流派、230+ 怪物数据库' in html
    assert html.count('data-status="live"') == 25
    assert html.count('target="_blank" rel="noopener noreferrer">访问项目 ↗</a>') == 25


def test_projects_section_includes_live_mergeanuke_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>Merge a Nuke! Guide</h3>' in html
    assert 'href="https://mergeanuke.space/"' in html
    assert '<span>19 · 已上线</span><span>核弹合成攻略站</span>' in html
    assert '可兑换代码、指挥官与突变情报、进度强度排行和合成计算器' in html


def test_projects_section_includes_live_aiscanner_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>AI Scanner</h3>' in html
    assert 'href="https://aiscanner.run/"' in html
    assert '<span>20 · 已上线</span><span>AI 文本检测工具</span>' in html
    assert '浏览器端免费检测' in html
    assert '多模型深度扫描、置信度和逐句原因说明' in html


def test_projects_section_includes_live_rspeditor_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>RSP Editor</h3>' in html
    assert 'href="https://rspeditor.app/"' in html
    assert '<span>21 · 已上线</span><span>AI 同款照片生成器</span>' in html
    assert '选择同款模板、上传照片并用 AI 在数秒内生成成片' in html
    assert '提示词库与交互式提示词构建器' in html


def test_projects_section_includes_live_remove_matcha_filter_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>Remove Matcha Filter</h3>' in html
    assert 'href="https://remove-matcha-filter.com/"' in html
    assert '<span>22 · 已上线</span><span>图片视频校色工具</span>' in html
    assert '修正抹茶绿色偏色的图片与短视频' in html
    assert '浏览器本地处理、效果对比与导出' in html
    assert '媒体文件无需上传服务器' in html


def test_projects_section_includes_live_deepseek_harness_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>DSH Field Guide</h3>' in html
    assert 'href="https://deepseekharness.site/"' in html
    assert '<span>23 · 已上线</span><span>DeepSeek 工具指南</span>' in html
    assert '独立的 DeepSeek Harness 实用指南' in html
    assert '经来源核验且标注版本' in html
    assert '安装、模型配置、Python SDK、插件与故障排查' in html


def test_projects_section_includes_live_polski_pilkarz_simulator_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>Polski Piłkarz Simulator</h3>' in html
    assert 'href="https://polskipilkarzsymulator.online/"' in html
    assert '<span>24 · 已上线</span><span>波兰足球生涯模拟器</span>' in html
    assert '可免费在线游玩 v1.90' in html
    assert '8400+ 家俱乐部与 101 个生涯事件' in html
    assert '比赛胜率计算器和新手指南' in html


def test_projects_section_includes_live_burnt_for_you_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>burnt for you</h3>' in html
    assert 'href="https://burncd.xyz/"' in html
    assert '<span>25 · 已上线</span><span>数字混音带制作器</span>' in html
    assert '挑选歌曲、写下留言并生成数字混音带 CD' in html
    assert '通过单个链接分享' in html
    assert '无需注册，每首歌以 30 秒片段播放' in html
