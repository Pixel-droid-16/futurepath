const FP_LOCALES = ["en", "ms", "zh"];
const FP_TEXT = {
  "Home": ["Home", "Utama", "首页"],
  "Start": ["Start", "Mula", "开始"],
  "Results": ["Results", "Keputusan", "结果"],
  "Choose start": ["Choose start", "Pilih cara bermula", "选择开始方式"],
  "Check profile": ["Check profile", "Semak profil", "检查档案"],
  "Pathway": ["Pathway", "Laluan", "学习路径"],
  "Signals": ["Signals", "Isyarat", "趋势信号"],
  "About": ["About", "Perihal", "关于"],
  "The world of work is changing.": ["The world of work is changing.", "Dunia pekerjaan sedang berubah.", "工作世界正在变化。"],
  "Find your place in it.": ["Find your place in it.", "Cari tempat anda di dalamnya.", "找到属于你的位置。"],
  "Whether you’re returning to work, facing a restructuring or just starting out, FuturePath shows which future roles fit your skills, why, and an affordable path to get there.": ["Whether you’re returning to work, facing a restructuring or just starting out, FuturePath shows which future roles fit your skills, why, and an affordable path to get there.", "Sama ada anda kembali bekerja, menghadapi penstrukturan semula atau baru memulakan kerjaya, FuturePath menunjukkan kerjaya masa depan yang sesuai dengan kemahiran anda, sebabnya dan laluan pembelajaran mampu milik untuk mencapainya.", "无论你是重返职场、面临重组，还是刚开始职业生涯，FuturePath 都会展示哪些未来职业适合你的技能、原因，以及可负担的学习路径。"],
  "Returning to work": ["Returning to work", "Kembali bekerja", "重返职场"],
  "Facing restructuring": ["Facing restructuring", "Menghadapi penstrukturan semula", "面临组织调整"],
  "Career switchers": ["Career switchers", "Penukar kerjaya", "转行人士"],
  "Fresh graduates": ["Fresh graduates", "Graduan baharu", "应届毕业生"],
  "Build my profile": ["Build my profile", "Bina profil saya", "建立我的档案"],
  "future roles": ["future roles", "kerjaya masa depan", "未来职业"],
  "dated signals": ["dated signals", "isyarat bertarikh", "有日期的趋势信号"],
  "checked courses": ["checked courses", "kursus yang disemak", "已核查课程"],
  "UP NEXT": ["UP NEXT", "SETERUSNYA", "接下来"],
  "signals": ["signals", "isyarat", "条信号"],
  "new this week": ["new this week", "baharu minggu ini", "本周新增"],
  "since last fetch": ["since last fetch", "sejak pengambilan terakhir", "距上次获取"],
  "See all signals →": ["See all signals →", "Lihat semua isyarat →", "查看所有信号 →"],
  "WHY NOW": ["WHY NOW", "MENGAPA SEKARANG", "为何是现在"],
  "Future-Ready Career Navigator": ["Future-Ready Career Navigator", "Panduan Kerjaya Bersedia untuk Masa Depan", "面向未来的职业导航"],
  "of Malaysian professionals use AI at work, but only 26% have had formal training.": ["of Malaysian professionals use AI at work, but only 26% have had formal training.", "profesional di Malaysia menggunakan AI di tempat kerja, tetapi hanya 26% pernah menerima latihan formal.", "的马来西亚专业人士在工作中使用 AI，但只有 26% 接受过正式培训。"],
  "workers will need reskilling within the next 3–5 years.": ["workers will need reskilling within the next 3–5 years.", "pekerja perlu meningkatkan kemahiran dalam tempoh 3–5 tahun akan datang.", "名劳动者将在未来 3–5 年内需要重新培训技能。"],
  "FUTURE SKILLS RADAR": ["FUTURE SKILLS RADAR", "RADAR KEMAHIRAN MASA DEPAN", "未来技能雷达"],
  "Future Skills Radar": ["Future Skills Radar", "Radar Kemahiran Masa Depan", "未来技能雷达"],
  "56%": ["56%", "56%", "56%"],
  "600,000+": ["600,000+", "600,000+", "60 万+"],
  "Hays Asia Salary Guide 2025": ["Hays Asia Salary Guide 2025", "Hays Asia Salary Guide 2025", "Hays 亚洲薪酬指南 2025"],
  "MOSTI": ["MOSTI", "MOSTI", "MOSTI"],
  "No course verification dates recorded": ["No course verification dates recorded", "Tiada tarikh pengesahan kursus direkodkan", "未记录课程核查日期"],
  "Provisional": ["Provisional", "Sementara", "暂定"],
  "Readiness unknown": ["Readiness unknown", "Tahap kesiapsiagaan tidak diketahui", "准备度未知"],
  "Interest fit unknown": ["Interest fit unknown", "Padanan minat tidak diketahui", "兴趣匹配未知"],
  "Interest fit: Take the optional RIASEC interest quiz to add it.": ["Interest fit: Take the optional RIASEC interest quiz to add it.", "Padanan minat: Jawab kuiz minat RIASEC pilihan untuk menambahkannya.", "兴趣匹配：完成可选的 RIASEC 兴趣测验即可加入兴趣匹配。"],
  "Basic": ["Basic", "Asas", "基础"],
  "Working": ["Working", "Boleh bekerja", "熟练应用"],
  "Strong": ["Strong", "Mahir", "精通"],
  "News": ["News", "Berita", "新闻"],
  "Research": ["Research", "Penyelidikan", "研究"],
  "Dataset": ["Dataset", "Set data", "数据集"],
  "Emerging": ["Emerging", "Meningkat", "上升"],
  "Declining": ["Declining", "Menurun", "下降"],
  "LIVE SIGNAL FEED": ["LIVE SIGNAL FEED", "SUAPAN ISYARAT LANGSUNG", "实时趋势信息"],
  "SAMPLE SIGNAL FEED": ["SAMPLE SIGNAL FEED", "CONTOH SUAPAN ISYARAT", "示例趋势信息"],
  "Business & Finance": ["Business & Finance", "Perniagaan & Kewangan", "商业与金融"],
  "Healthcare & Life Sciences": ["Healthcare & Life Sciences", "Penjagaan Kesihatan & Sains Hayat", "医疗与生命科学"],
  "Sustainability & Green Economy": ["Sustainability & Green Economy", "Kemampanan & Ekonomi Hijau", "可持续发展与绿色经济"],
  "Engineering & Manufacturing": ["Engineering & Manufacturing", "Kejuruteraan & Pembuatan", "工程与制造"],
  "Education & Creative": ["Education & Creative", "Pendidikan & Kreatif", "教育与创意"],
  "Assess this skill before claiming a gap": ["Assess this skill before claiming a gap", "Nilai kemahiran ini sebelum menganggapnya sebagai jurang", "在认定存在技能差距前先评估此技能"],
  "Take the interest quiz to add interest fit.": ["Take the interest quiz to add interest fit.", "Jawab kuiz minat untuk menambah padanan minat.", "完成兴趣测验以加入兴趣匹配。"],
  "Moderate AI adoption": ["Moderate AI adoption", "Penggunaan AI sederhana", "温和的 AI 采用"],
  "Rapid AI adoption": ["Rapid AI adoption", "Penggunaan AI pantas", "快速的 AI 采用"],
  "AI tools support selected workflows with staged adoption.": ["AI tools support selected workflows with staged adoption.", "Alat AI menyokong aliran kerja terpilih dengan penggunaan secara berperingkat.", "AI 工具以分阶段方式支持部分工作流程。"],
  "AI adoption continues at roughly the pace employers reported in the WEF Future of Jobs Report 2025. Signals are used as they are.": ["AI adoption continues at roughly the pace employers reported in the WEF Future of Jobs Report 2025. Signals are used as they are.", "Penggunaan AI berterusan pada kadar yang hampir sama seperti dilaporkan majikan dalam WEF Future of Jobs Report 2025. Isyarat digunakan seperti yang diterbitkan.", "AI 采用速度大致延续雇主在《WEF 2025 年未来就业报告》中报告的水平。趋势信号按原样使用。"],
  "Rapid rollout: AI tools become widely embedded across workflows in this hypothetical scenario.": ["Rapid rollout: AI tools become widely embedded across workflows in this hypothetical scenario.", "Pelaksanaan pantas: alat AI digunakan secara meluas dalam aliran kerja dalam senario hipotesis ini.", "快速推广：在此假设情景中，AI 工具广泛融入各项工作流程。"],
  "What's rising, what's fading": ["What's rising, what's fading", "Kemahiran yang meningkat dan merosot", "哪些技能正在上升，哪些正在减弱"],
  "↑ Rising skills": ["↑ Rising skills", "↑ Kemahiran meningkat", "↑ 上升技能"],
  "↓ Declining skills": ["↓ Declining skills", "↓ Kemahiran menurun", "↓ 下降技能"],
  "See the signals behind this →": ["See the signals behind this →", "Lihat isyarat di sebaliknya →", "查看背后的趋势信号 →"],
  "Every role links to the UN SDGs": ["Every role links to the UN SDGs", "Setiap kerjaya dikaitkan dengan SDG PBB", "每个职业均关联联合国可持续发展目标"],
  "of the 17 goals are linked to our roles (highlighted).": ["of the 17 goals are linked to our roles (highlighted).", "daripada 17 matlamat dikaitkan dengan kerjaya kami (ditandakan).", "项可持续发展目标与我们的职业相关联（已突出显示），共 17 项。"],
  "SDG icons © United Nations, used for information only; no endorsement implied.": ["SDG icons © United Nations, used for information only; no endorsement implied.", "Ikon SDG © Pertubuhan Bangsa-Bangsa Bersatu, digunakan untuk maklumat sahaja; tiada sokongan rasmi dinyatakan.", "SDG 图标 © 联合国，仅供信息参考；不代表联合国认可。"],
  "LEARNING PATHWAY": ["LEARNING PATHWAY", "LALUAN PEMBELAJARAN", "学习路径"],
  "hours": ["hours", "jam", "小时"],
  "weeks": ["weeks", "minggu", "周"],
  "Builds:": ["Builds:", "Membangunkan:", "培养："],
  "Skill contribution to the SDGs": ["Skill contribution to the SDGs", "Sumbangan kemahiran kepada SDG", "技能对可持续发展目标的潜在贡献"],
  "No checked course yet": ["No checked course yet", "Belum ada kursus yang disemak", "暂无已核查课程"],
  "Other options:": ["Other options:", "Pilihan lain:", "其他选项："],
  "How this career may contribute to the SDGs": ["How this career may contribute to the SDGs", "Cara kerjaya ini boleh menyumbang kepada SDG", "此职业可能如何为可持续发展目标作出贡献"],
  "Potential alignment only; real contribution depends on how the work is carried out and its outcomes.": ["Potential alignment only; real contribution depends on how the work is carried out and its outcomes.", "Ini hanya potensi penjajaran; sumbangan sebenar bergantung pada cara kerja dilakukan dan hasilnya.", "这仅表示潜在关联；实际贡献取决于工作方式及其成果。"],
  "Build through practice": ["Build through practice", "Bina kemahiran melalui latihan", "通过实践提升"],
  "Practice verified skills and ask for feedback as you learn.": ["Practice verified skills and ask for feedback as you learn.", "Amalkan kemahiran yang telah disahkan dan minta maklum balas semasa belajar.", "练习已确认的技能，并在学习过程中征求反馈。"],
  "STEP 4 OF 4": ["STEP 4 OF 4", "LANGKAH 4 DARIPADA 4", "第 4 步，共 4 步"],
  "STEP": ["STEP", "LANGKAH", "第"],
  "OF 4": ["OF 4", "DARIPADA 4", "步，共 4 步"],
  "SAVED PEOPLE (": ["SAVED PEOPLE (", "PROFIL TERSIMPAN (", "已保存的档案（"],
  "Your future roles": ["Your future roles", "Kerjaya masa depan anda", "适合你的未来职业"],
  "+ Analyse a different CV": ["+ Analyse a different CV", "+ Analisis CV yang lain", "+ 分析另一份简历"],
  "Saved people:": ["Saved people:", "Profil tersimpan:", "已保存的档案："],
  "⚠ Estimate, not a prediction.": ["⚠ Estimate, not a prediction.", "⚠ Anggaran, bukan ramalan.", "⚠ 这是估算，不是预测。"],
  "Scores combine the skills you have with dated trend signals, using the formula shown on each role. They show where today's evidence points, not what will happen. You decide what to do with them.": ["Scores combine the skills you have with dated trend signals, using the formula shown on each role. They show where today's evidence points, not what will happen. You decide what to do with them.", "Skor menggabungkan kemahiran anda dengan isyarat trend bertarikh menggunakan formula yang ditunjukkan pada setiap kerjaya. Skor menunjukkan arah bukti semasa, bukan perkara yang pasti berlaku. Anda menentukan tindakan seterusnya.", "分数根据每个职业所示公式，将你的技能与有日期的趋势信号结合。它反映当前证据所指方向，而非未来必然结果。你可以自行决定如何使用这些信息。"],
  "AI disruption scenario": ["AI disruption scenario", "Senario gangguan AI", "AI 冲击情景"],
  "More than one future": ["More than one future", "Lebih daripada satu masa depan", "不止一种未来"],
  "AI adoption speeds up. Every AI-related trend signal (its headline or summary mentions AI, automation, machine learning or robots) counts double; other signals count as usual.": ["AI adoption speeds up. Every AI-related trend signal (its headline or summary mentions AI, automation, machine learning or robots) counts double; other signals count as usual.", "Penggunaan AI meningkat dengan pantas. Setiap isyarat trend berkaitan AI (tajuk atau ringkasannya menyebut AI, automasi, pembelajaran mesin atau robot) dikira dua kali; isyarat lain dikira seperti biasa.", "AI 采用速度加快。每条与 AI 相关的趋势信号（标题或摘要提到 AI、自动化、机器学习或机器人）按双倍计算；其他信号照常计算。"],
  "No AI-related signals, so demand is unchanged": ["No AI-related signals, so demand is unchanged", "Tiada isyarat berkaitan AI, jadi permintaan tidak berubah", "没有与 AI 相关的信号，因此需求不变"],
  "counts double (AI)": ["counts double (AI)", "dikira dua kali (AI)", "按双倍计算（AI）"],
  "A modelling assumption chosen by the FuturePath team, not a forecast. Your skill match is unchanged.": ["A modelling assumption chosen by the FuturePath team, not a forecast. Your skill match is unchanged.", "Andaian pemodelan yang dipilih oleh pasukan FuturePath, bukan ramalan. Padanan kemahiran anda tidak berubah.", "这是 FuturePath 团队设定的建模假设，并非预测。你的技能匹配度保持不变。"],
  "Baseline estimate, not a prediction.": ["Baseline estimate, not a prediction.", "Anggaran asas, bukan ramalan.", "基线估算，并非预测。"],
  "Take the optional RIASEC interest quiz to add interest fit.": ["Take the optional RIASEC interest quiz to add interest fit.", "Jawab kuiz minat RIASEC pilihan untuk menambah padanan minat.", "完成可选的 RIASEC 兴趣测验以加入兴趣匹配。"],
  "You share Realistic, Investigative interests with this career.": ["You share Realistic, Investigative interests with this career.", "Anda berkongsi minat Realistik dan Investigatif dengan kerjaya ini.", "你与此职业都偏向现实型、研究型兴趣。"],
  "Your strongest interests differ from this career’s.": ["Your strongest interests differ from this career’s.", "Minat utama anda berbeza daripada kerjaya ini.", "你最强的兴趣类型与此职业不同。"],
  "Human-led with AI support": ["Human-led with AI support", "Diterajui manusia dengan sokongan AI", "以人为主，AI 辅助"],
  "Selective AI assistance": ["Selective AI assistance", "Bantuan AI terpilih", "选择性使用 AI 辅助"],
  "AI co-pilot likely": ["AI co-pilot likely", "AI berkemungkinan menjadi pembantu kerja", "AI 可能成为协作助手"],
  "Major workflow redesign": ["Major workflow redesign", "Perubahan besar aliran kerja", "工作流程重大重构"],
  "Predominantly human-led": ["Predominantly human-led", "Kebanyakannya diterajui manusia", "主要由人主导"],
  "Human oversight": ["Human oversight", "Pengawasan manusia", "人工监督"],
  "Selectively assisted": ["Selectively assisted", "Dibantu secara terpilih", "选择性辅助"],
  "Technology & AI": ["Technology & AI", "Teknologi & AI", "技术与人工智能"],
  "Finance": ["Finance", "Kewangan", "金融"],
  "Healthcare": ["Healthcare", "Penjagaan kesihatan", "医疗健康"],
  "Energy & Environment": ["Energy & Environment", "Tenaga & Alam Sekitar", "能源与环境"],
  "Engineering": ["Engineering", "Kejuruteraan", "工程"],
  "Education & Design": ["Education & Design", "Pendidikan & Reka Bentuk", "教育与设计"],
  "Fix or assemble machines, devices or equipment": ["Fix or assemble machines, devices or equipment", "Membaiki atau memasang mesin, peranti atau peralatan", "维修或组装机器、设备或器材"],
  "Work out why something isn't working by testing ideas": ["Work out why something isn't working by testing ideas", "Mencari punca masalah dengan menguji idea", "通过测试想法找出问题原因"],
  "Design posters, videos, layouts or websites": ["Design posters, videos, layouts or websites", "Mereka bentuk poster, video, susun atur atau laman web", "设计海报、视频、版式或网站"],
  "Teach or explain things to other people": ["Teach or explain things to other people", "Mengajar atau menerangkan sesuatu kepada orang lain", "教导或向他人解释事物"],
  "Persuade people to try an idea or a product": ["Persuade people to try an idea or a product", "Meyakinkan orang untuk mencuba idea atau produk", "说服他人尝试某个想法或产品"],
  "Keep records, files or schedules well organised": ["Keep records, files or schedules well organised", "Menyusun rekod, fail atau jadual dengan teratur", "有条理地整理记录、文件或日程"],
  "Work outdoors or with my hands, on a farm, site or workshop": ["Work outdoors or with my hands, on a farm, site or workshop", "Bekerja di luar atau menggunakan tangan di ladang, tapak atau bengkel", "在户外或农场、工地、车间动手工作"],
  "Analyse numbers or data to find patterns": ["Analyse numbers or data to find patterns", "Menganalisis nombor atau data untuk mencari corak", "分析数字或数据以发现规律"],
  "Write stories, captions or articles": ["Write stories, captions or articles", "Menulis cerita, kapsyen atau artikel", "撰写故事、说明文字或文章"],
  "Help people with their problems or look after them": ["Help people with their problems or look after them", "Membantu orang menyelesaikan masalah atau menjaga mereka", "帮助他人解决问题或照顾他人"],
  "Lead a project or a group and make the decisions": ["Lead a project or a group and make the decisions", "Memimpin projek atau kumpulan dan membuat keputusan", "带领项目或团队并作出决策"],
  "Check details carefully so there are no mistakes": ["Check details carefully so there are no mistakes", "Memeriksa butiran dengan teliti supaya tiada kesilapan", "仔细检查细节以避免错误"],
  "Operate tools, vehicles or machinery": ["Operate tools, vehicles or machinery", "Mengendalikan alatan, kenderaan atau mesin", "操作工具、车辆或机械"],
  "Learn how things work in science or technology": ["Learn how things work in science or technology", "Mempelajari cara sesuatu berfungsi dalam sains atau teknologi", "学习科学或技术中的事物如何运作"],
  "Come up with original ideas instead of following a set method": ["Come up with original ideas instead of following a set method", "Menghasilkan idea asli dan bukannya mengikut kaedah tetap", "提出原创想法，而不是遵循固定方法"],
  "Work in a team where people support each other": ["Work in a team where people support each other", "Bekerja dalam pasukan yang saling menyokong", "在彼此支持的团队中工作"],
  "Start or grow a small business": ["Start or grow a small business", "Memulakan atau mengembangkan perniagaan kecil", "创办或发展小型企业"],
  "Follow clear procedures and work with spreadsheets": ["Follow clear procedures and work with spreadsheets", "Mengikuti prosedur yang jelas dan menggunakan hamparan elektronik", "遵循明确流程并使用电子表格"],
  "Strongly dislike": ["Strongly dislike", "Sangat tidak suka", "非常不喜欢"],
  "Dislike": ["Dislike", "Tidak suka", "不喜欢"],
  "Not sure": ["Not sure", "Tidak pasti", "不确定"],
  "Like": ["Like", "Suka", "喜欢"],
  "Strongly like": ["Strongly like", "Sangat suka", "非常喜欢"],
  "Realistic": ["Realistic", "Realistik", "现实型"],
  "Investigative": ["Investigative", "Investigatif", "研究型"],
  "Artistic": ["Artistic", "Artistik", "艺术型"],
  "Social": ["Social", "Sosial", "社会型"],
  "Enterprising": ["Enterprising", "Keusahawanan", "企业型"],
  "Conventional": ["Conventional", "Konvensional", "常规型"],
  "Moderate AI disruption": ["Moderate AI disruption", "Gangguan AI sederhana", "温和的 AI 冲击"],
  "Fast AI disruption": ["Fast AI disruption", "Gangguan AI pantas", "快速的 AI 冲击"],
  "Adjust the weights": ["Adjust the weights", "Laraskan pemberat", "调整权重"],
  "Reset": ["Reset", "Tetapkan semula", "重置"],
  "You are in control: change how much each part counts and the ranking updates.": ["You are in control: change how much each part counts and the ranking updates.", "Anda boleh mengubah kepentingan setiap komponen dan kedudukan akan dikemas kini.", "你可以调整各项因素的权重，排名也会随之更新。"],
  "Skills you have": ["Skills you have", "Kemahiran yang anda miliki", "你已具备的技能"],
  "Future demand": ["Future demand", "Permintaan masa depan", "未来需求"],
  "WHAT CHANGED": ["WHAT CHANGED", "APA YANG BERUBAH", "变化内容"],
  "Top matched roles": ["Top matched roles", "Kerjaya paling sepadan", "匹配度最高的职业"],
  "Sorted by match": ["Sorted by match", "Disusun mengikut padanan", "按匹配度排序"],
  "Skills": ["Skills", "Kemahiran", "技能"],
  "Why this role, signals and interest fit": ["Why this role, signals and interest fit", "Sebab kerjaya, isyarat dan minat ini sepadan", "职业、趋势信号与兴趣匹配原因"],
  "Interest fit:": ["Interest fit:", "Padanan minat:", "兴趣匹配："],
  "Signals last updated:": ["Signals last updated:", "Isyarat terakhir dikemas kini:", "趋势信号最近更新："],
  "Demand": ["Demand", "Permintaan", "需求"],
  "Demand ±": ["Demand ±", "Permintaan ±", "需求 ±"],
  "See pathway →": ["See pathway →", "Lihat laluan →", "查看学习路径 →"],
  "↑ Rising roles": ["↑ Rising roles", "↑ Kerjaya meningkat", "↑ 上升职业"],
  "↓ Declining roles": ["↓ Declining roles", "↓ Kerjaya menurun", "↓ 下降职业"],
  "No career in our catalogue has net declining demand signals right now.": ["No career in our catalogue has net declining demand signals right now.", "Buat masa ini, tiada kerjaya dalam katalog kami yang mempunyai isyarat permintaan menurun secara bersih.", "目前目录中没有职业呈现净需求下降信号。"],
  "Role demand changes with the scenario. Skill outlook uses the signals as published.": ["Role demand changes with the scenario. Skill outlook uses the signals as published.", "Permintaan kerjaya berubah mengikut senario. Tinjauan kemahiran menggunakan isyarat seperti yang diterbitkan.", "职业需求会随情景变化。技能趋势依据已发布的信号计算。"],
  "TREND SIGNALS": ["TREND SIGNALS", "ISYARAT TREND", "趋势信号"],
  "The evidence behind every score": ["The evidence behind every score", "Bukti di sebalik setiap skor", "每个分数背后的证据"],
  "Curated reports form the baseline; new items arrive from news, research and dataset feeds, each dated and sourced.": ["Curated reports form the baseline; new items arrive from news, research and dataset feeds, each dated and sourced.", "Laporan pilihan menjadi asas; item baharu diperoleh daripada suapan berita, penyelidikan dan set data, masing-masing dengan sumber dan tarikh.", "精选报告构成基线；新闻、研究和数据集信息会持续补充，每条均标明来源和日期。"],
  "LAST UPDATED": ["LAST UPDATED", "KEMAS KINI TERAKHIR", "最近更新"],
  "LAST REFRESH": ["LAST REFRESH", "MUAT SEMULA TERAKHIR", "最近刷新"],
  "Refresh from live feeds": ["Refresh from live feeds", "Muat semula daripada suapan langsung", "从实时信息源刷新"],
  "All": ["All", "Semua", "全部"],
  "↑ Emerging": ["↑ Emerging", "↑ Meningkat", "↑ 上升"],
  "↓ Declining": ["↓ Declining", "↓ Menurun", "↓ 下降"],
  "Roles:": ["Roles:", "Kerjaya:", "职业："],
  "Open source ↗": ["Open source ↗", "Buka sumber ↗", "打开来源 ↗"],
  "ABOUT & AI DISCLOSURE": ["ABOUT & AI DISCLOSURE", "TENTANG & PENJELASAN AI", "关于与 AI 说明"],
  "AI supports.": ["AI supports.", "AI membantu.", "AI 提供辅助。"],
  "Humans decide.": ["Humans decide.", "Manusia membuat keputusan.", "由人来决定。"],
  "AI models used": ["AI models used", "Model AI yang digunakan", "使用的 AI 模型"],
  "Claude by Anthropic: tags trend signals, extracts skills from CVs": ["Claude by Anthropic: tags trend signals, extracts skills from CVs", "Claude oleh Anthropic: menandai isyarat trend dan mengekstrak kemahiran daripada CV", "Anthropic 的 Claude：为趋势信号添加标签并从简历中提取技能"],
  "Keyword matching: used for CV skills and signal tagging when Claude is not configured": ["Keyword matching: used for CV skills and signal tagging when Claude is not configured", "Padanan kata kunci digunakan untuk kemahiran CV dan penandaan isyarat apabila Claude tidak dikonfigurasi", "未配置 Claude 时，使用关键词匹配简历技能并为趋势信号添加标签"],
  "No model scores, ranks or orders anything.": ["No model scores, ranks or orders anything.", "Tiada model yang memberikan skor, kedudukan atau susunan.", "没有任何模型负责评分、排名或排序。"],
  "Data sources": ["Data sources", "Sumber data", "数据来源"],
  "Fairness": ["Fairness", "Kesaksamaan", "公平性"],
  "Privacy": ["Privacy", "Privasi", "隐私"],
  "AI never decides a score or a career for you.": ["AI never decides a score or a career for you.", "AI tidak pernah menentukan skor atau kerjaya untuk anda.", "AI 不会替你决定分数或职业。"],
  "Age, gender, ethnicity, religion and contact details are never collected as scoring inputs; scores use only confirmed skills, demand signals and optional interests.": ["Age, gender, ethnicity, religion and contact details are never collected as scoring inputs; scores use only confirmed skills, demand signals and optional interests.", "Umur, jantina, etnik, agama dan maklumat hubungan tidak digunakan untuk pengiraan skor; skor hanya menggunakan kemahiran yang disahkan, isyarat permintaan dan minat pilihan.", "年龄、性别、族裔、宗教及联系方式不会作为评分依据；评分只使用已确认的技能、需求信号和可选兴趣。"],
  "CVs are read in memory and discarded. This demo keeps one shared profile on the server, so use a fictional CV.": ["CVs are read in memory and discarded. This demo keeps one shared profile on the server, so use a fictional CV.", "CV dibaca dalam memori dan kemudian dibuang. Demo ini menyimpan profil bersama pada pelayan, jadi gunakan CV rekaan.", "简历仅在内存中读取，之后即丢弃。本演示在服务器上使用共享档案，因此请使用虚构简历。"],
  "Checked catalog only": ["Checked catalog only", "Katalog yang disemak sahaja", "仅使用已核查目录"],
  "Claude only reads and labels": ["Claude only reads and labels", "Claude hanya membaca dan menandai", "Claude 仅负责读取和标注"],
  "Fixed, published formulas": ["Fixed, published formulas", "Formula tetap yang diterbitkan", "使用固定且公开的公式"],
  "FuturePath helps people in Malaysia whose jobs are changing because of AI see which future roles fit them, why, and how to get there with free or low-cost learning.": ["FuturePath helps people in Malaysia whose jobs are changing because of AI see which future roles fit them, why, and how to get there with free or low-cost learning.", "FuturePath membantu rakyat Malaysia yang pekerjaannya berubah akibat AI melihat kerjaya masa depan yang sesuai, sebabnya dan cara mencapainya melalui pembelajaran percuma atau berkos rendah.", "FuturePath 帮助因 AI 而面临工作变化的马来西亚民众了解适合自己的未来职业、原因，以及通过免费或低价学习实现目标的方式。"],
  "It tags news against our catalog and picks out CV skills. You confirm every skill.": ["It tags news against our catalog and picks out CV skills. You confirm every skill.", "Ia menandai berita berdasarkan katalog dan mengenal pasti kemahiran dalam CV. Anda mengesahkan setiap kemahiran.", "它会根据目录标注新闻，并从简历中提取技能。每项技能都由你确认。"],
  "The AI cannot invent jobs, courses or statistics.": ["The AI cannot invent jobs, courses or statistics.", "AI tidak boleh mereka cipta pekerjaan, kursus atau statistik.", "AI 不会编造职业、课程或统计数据。"],
  "18 quick questions based on the Holland RIASEC interest model. Your answers add an interest-fit score. They never hide any role, and you can skip this.": ["18 quick questions based on the Holland RIASEC interest model. Your answers add an interest-fit score. They never hide any role, and you can skip this.", "18 soalan ringkas berdasarkan model minat Holland RIASEC. Jawapan anda menambah skor padanan minat. Tiada kerjaya disembunyikan dan anda boleh melangkau langkah ini.", "共 18 道基于 Holland RIASEC 兴趣模型的简短问题。你的回答会加入兴趣匹配分数，不会隐藏任何职业，也可以跳过。"],
  "Your CV is read once to pick out skills and is never stored. Only the skills you approve are saved, and personal details are never used in scoring.": ["Your CV is read once to pick out skills and is never stored. Only the skills you approve are saved, and personal details are never used in scoring.", "CV anda dibaca sekali untuk mengenal pasti kemahiran dan tidak disimpan. Hanya kemahiran yang anda luluskan disimpan dan maklumat peribadi tidak digunakan untuk pengiraan skor.", "简历只读取一次以提取技能，不会保存。系统只保存你确认的技能，个人信息不会用于评分。"],
  "KEY": ["KEY", "KUNCI", "密钥"],
  "LLM": ["LLM", "LLM", "大语言模型"],
  "SDGs": ["SDGs", "SDG", "可持续发展目标"],
  "courses": ["courses", "kursus", "门课程"],
  "roles": ["roles", "kerjaya", "种职业"],
  "● configured": ["● configured", "● dikonfigurasi", "● 已配置"],
  "● keyword fallback": ["● keyword fallback", "● sandaran kata kunci", "● 关键词备用方案"],
  "← Back to results": ["← Back to results", "← Kembali ke keputusan", "← 返回结果"],
  "Start →": ["Start →", "Mula →", "开始 →"],
  "· Skill matching: exact skills from our catalogue, at the level you confirmed.": ["· Skill matching: exact skills from our catalogue, at the level you confirmed.", "· Padanan kemahiran: kemahiran tepat daripada katalog pada tahap yang anda sahkan.", "· 技能匹配：使用目录中的技能，并采用你确认的熟练程度。"],
  "Google News, arXiv and the Anthropic Economic Index. New items are tagged by Claude (or keywords without an API key), checked against our catalogue and stored with their source and date.": ["Google News, arXiv and the Anthropic Economic Index. New items are tagged by Claude (or keywords without an API key), checked against our catalogue and stored with their source and date.", "Google News, arXiv dan Anthropic Economic Index. Item baharu ditandai oleh Claude (atau kata kunci tanpa kunci API), disemak berdasarkan katalog dan disimpan bersama sumber serta tarikhnya.", "数据来源包括 Google 新闻、arXiv 和 Anthropic Economic Index。新条目由 Claude 标注（没有 API 密钥时使用关键词），并根据目录检查后连同来源和日期保存。"],
  "Strength (1–5) is a team judgement of how direct and large the evidence is (curated reports); feed items are capped at 3. A signal counts in full for a career it names, at reduced weight through a required skill, and halves in weight every 12 months.": ["Strength (1–5) is a team judgement of how direct and large the evidence is (curated reports); feed items are capped at 3. A signal counts in full for a career it names, at reduced weight through a required skill, and halves in weight every 12 months.", "Kekuatan (1–5) ialah penilaian pasukan tentang ketegasan dan keluasan bukti (laporan pilihan); item suapan dihadkan kepada 3. Isyarat diberi nilai penuh bagi kerjaya yang dinamakan, nilai lebih rendah melalui kemahiran yang diperlukan, dan nilainya berkurang separuh setiap 12 bulan.", "强度（1–5）是团队对证据直接性和覆盖范围的判断（适用于精选报告）；信息源条目的强度上限为 3。信号对明确提及的职业按全权重计分，通过必需技能关联时权重较低，并每 12 个月减半。"],
  "Curated & verified": ["Curated & verified", "Dipilih dan disahkan", "精选并核查"],
  "Tagged by Claude": ["Tagged by Claude", "Ditandai oleh Claude", "由 Claude 标注"],
  "Keyword fallback": ["Keyword fallback", "Sandaran kata kunci", "关键词备用方案"],
  "General context": ["General context", "Konteks umum", "一般背景"],
  "Linked through skills only": ["Linked through skills only", "Dikaitkan melalui kemahiran sahaja", "仅通过技能关联"],
  "Not refreshed yet": ["Not refreshed yet", "Belum dimuat semula", "尚未刷新"],
  "English": ["English", "Bahasa Melayu", "English"],
  "BM": ["BM", "BM", "简体中文"],
  "简体中文": ["简体中文", "English", "English"],
  "e.g. Administrative assistant at a logistics company": ["e.g. Administrative assistant at a logistics company", "cth. Pembantu pentadbiran di syarikat logistik", "例如：物流公司的行政助理"],
  "e.g. Diploma in Office Management": ["e.g. Diploma in Office Management", "cth. Diploma Pengurusan Pejabat", "例如：办公室管理文凭"],
  "Bahasa Melayu, English": ["Bahasa Melayu, English", "Bahasa Melayu, English", "马来语、英语"],
  "Search skills…": ["Search skills…", "Cari kemahiran…", "搜索技能…"],
  "Name (optional)": ["Name (optional)", "Nama (pilihan)", "姓名（选填）"],
  "Your name": ["Your name", "Nama anda", "你的姓名"],
  "Headline (optional)": ["Headline (optional)", "Tajuk profil (pilihan)", "个人简介标题（选填）"],
  "e.g. Junior data analyst": ["e.g. Junior data analyst", "cth. Penganalisis data junior", "例如：初级数据分析师"],
  "Language": ["Language", "Bahasa", "语言"],
  "These are potential links, not guaranteed outcomes.": ["These are potential links, not guaranteed outcomes.", "Ini ialah potensi perkaitan, bukan hasil yang dijamin.", "这些只是潜在关联，并非结果保证。"],
  "SDG connection not documented for this skill.": ["SDG connection not documented for this skill.", "Hubungan dengan SDG belum didokumenkan untuk kemahiran ini.", "此技能尚未记录与可持续发展目标的关联。"],
  "Free": ["Free", "Percuma", "免费"],
  "Low cost": ["Low cost", "Kos rendah", "低价"],
  "Low cost (paid certificate)": ["Low cost (paid certificate)", "Kos rendah (sijil berbayar)", "低价（付费证书）"],
  "HRD Corp claimable (confirm per run)": ["HRD Corp claimable (confirm per run)", "Boleh dituntut melalui HRD Corp (sahkan bagi setiap pengambilan)", "可申请 HRD Corp 资助（每期开课前请确认）"],
  "Duration unknown": ["Duration unknown", "Tempoh tidak diketahui", "时长未知"],
  "Review skill requirements": ["Review skill requirements", "Semak keperluan kemahiran", "查看技能要求"],
  "No dated signal": ["No dated signal", "Tiada isyarat bertarikh", "没有带日期的趋势信号"],
  "OK": ["OK", "OK", "正常"],
  "Running": ["Running", "Sedang berjalan", "运行中"],
  "Loading": ["Loading", "Memuatkan", "加载中"],
  "Reading your CV…": ["Reading your CV…", "Membaca CV anda…", "正在读取简历…"],
  "Read my CV": ["Read my CV", "Baca CV saya", "读取我的简历"],
  "Saving…": ["Saving…", "Menyimpan…", "正在保存…"],
  "Refreshing…": ["Refreshing…", "Sedang dimuat semula…", "正在刷新…"],
  "Refresh signals": ["Refresh signals", "Muat semula isyarat", "刷新趋势信号"],
  "Source titles and course names are shown in their original language.": ["Source titles and course names are shown in their original language.", "Tajuk sumber dan nama kursus dipaparkan dalam bahasa asalnya.", "来源标题和课程名称以其原始语言显示。"],
  "Select a career": ["Select a career", "Pilih kerjaya", "选择职业"],
  "Choose a career on the results page": ["Choose a career on the results page", "Pilih kerjaya pada halaman hasil", "请在结果页面选择职业"],
  "Select a career to see its SDG connection.": ["Select a career to see its SDG connection.", "Pilih kerjaya untuk melihat kaitannya dengan SDG.", "选择职业以查看其与可持续发展目标的关联。"],
  "Assess first": ["Assess first", "Nilai dahulu", "先评估"],
  "Learning priority": ["Learning priority", "Keutamaan pembelajaran", "学习优先项"],
  "Unknown": ["Unknown", "Tidak diketahui", "未知"],
  "Demand uses the synthetic snapshot value.": ["Demand uses the synthetic snapshot value.", "Permintaan menggunakan nilai snapshot sintetik.", "需求依据合成快照值计算。"],
  "not linked yet": ["not linked yet", "belum dikaitkan", "尚未关联"],
  "linked": ["linked", "dikaitkan", "已关联"],
  "daily": ["daily", "setiap hari", "每天"],
  "Live feeds not checked yet; showing dated reports only": ["Live feeds not checked yet; showing dated reports only", "Suapan langsung belum disemak; laporan bertarikh sahaja dipaparkan", "实时信息源尚未检查；目前仅显示带日期的报告"],
  "Live feeds last checked": ["Live feeds last checked", "Suapan langsung terakhir disemak", "实时信息源上次检查时间"],
  "refreshed manually": ["refreshed manually", "dimuat semula secara manual", "手动刷新"],
  "No earlier ranking to compare yet. When new signals arrive, changes to your ranking will show here.": ["No earlier ranking to compare yet. When new signals arrive, changes to your ranking will show here.", "Belum ada kedudukan terdahulu untuk dibandingkan. Apabila isyarat baharu tiba, perubahan pada kedudukan anda akan dipaparkan di sini.", "目前没有可供比较的先前排名。收到新趋势信号后，排名变化会显示在这里。"],
  "Interest fit counts for 20%. Your strongest interests:": ["Interest fit counts for 20%. Your strongest interests:", "Padanan minat menyumbang 20%. Minat utama anda:", "兴趣匹配占 20%。你最突出的兴趣类型："],
  "quiz done": ["quiz done", "kuiz selesai", "已完成测验"],
  "no quiz": ["no quiz", "tiada kuiz", "未完成测验"],
  "skills": ["skills", "kemahiran", "项技能"],
  "saved": ["saved", "disimpan", "已保存"],
  "AI disclosure": ["AI disclosure", "Penjelasan AI", "AI 说明"],
  "Source code ↗": ["Source code ↗", "Kod sumber ↗", "源代码 ↗"],
  "Demo · synthetic": ["Demo · synthetic", "Demo · sintetik", "演示 · 合成数据"],
  "Dark": ["Dark", "Gelap", "深色"],
  "Light": ["Light", "Cerah", "浅色"],
  "PRISM": ["PRISM", "PRISM", "PRISM"],
  "← Return to original v2 experience": ["← Return to original v2 experience", "← Kembali ke pengalaman v2 asal", "← 返回原始 v2 体验"],
  "LIVE AI · SYNTHETIC DEMONSTRATION": ["LIVE AI · SYNTHETIC DEMONSTRATION", "AI LANGSUNG · DEMONSTRASI SINTETIK", "实时 AI · 合成示例演示"],
  "AI-assisted skill review": ["AI-assisted skill review", "Semakan kemahiran berbantu AI", "AI 辅助技能审核"],
  "Securely test the connected Claude or RunPod backend using synthetic CV text. You must confirm skills and proficiency before they are saved. The original group v2 mockup is preserved separately.": ["Securely test the connected Claude or RunPod backend using synthetic CV text. You must confirm skills and proficiency before they are saved. The original group v2 mockup is preserved separately.", "Uji bahagian belakang Claude atau RunPod yang disambungkan dengan selamat menggunakan teks CV sintetik. Anda mesti mengesahkan kemahiran dan tahap penguasaan sebelum disimpan. Mockup kumpulan v2 asal dikekalkan secara berasingan.", "使用合成简历文本安全测试已连接的 Claude 或 RunPod 后端。保存前必须确认技能和熟练程度。原始团队 v2 原型另行保留。"],
  "1. Supply synthetic CV text": ["1. Supply synthetic CV text", "1. Masukkan teks CV sintetik", "1. 提供合成简历文本"],
  "Only use a fictional CV. Do not submit real names, phone numbers, emails, medical details or confidential documents to external AI providers.": ["Only use a fictional CV. Do not submit real names, phone numbers, emails, medical details or confidential documents to external AI providers.", "Gunakan CV rekaan sahaja. Jangan hantar nama, nombor telefon, e-mel, butiran perubatan atau dokumen sulit sebenar kepada penyedia AI luar.", "仅使用虚构简历。请勿将真实姓名、电话号码、电子邮件、医疗信息或机密文件提交给外部 AI 服务商。"],
  "Synthetic CV extract": ["Synthetic CV extract", "Petikan CV sintetik", "合成简历摘录"],
  "Example: I used SQL queries and Python in a university data project...": ["Example: I used SQL queries and Python in a university data project...", "Contoh: Saya menggunakan pertanyaan SQL dan Python dalam projek data universiti...", "例如：我在大学数据项目中使用了 SQL 查询和 Python……"],
  "Extraction provider": ["Extraction provider", "Penyedia pengekstrakan", "提取服务商"],
  "Auto: RunPod → Claude → local fallback": ["Auto: RunPod → Claude → local fallback", "Automatik: RunPod → Claude → sandaran setempat", "自动：RunPod → Claude → 本地备用方案"],
  "Claude only (live API)": ["Claude only (live API)", "Claude sahaja (API langsung)", "仅使用 Claude（实时 API）"],
  "RunPod only (live GPU)": ["RunPod only (live GPU)", "RunPod sahaja (GPU langsung)", "仅使用 RunPod（实时 GPU）"],
  "Local dictionary (offline)": ["Local dictionary (offline)", "Kamus setempat (luar talian)", "本地词典（离线）"],
  "Checking backend configuration…": ["Checking backend configuration…", "Menyemak konfigurasi bahagian belakang…", "正在检查后端配置……"],
  "Extract suggested skills": ["Extract suggested skills", "Ekstrak kemahiran yang dicadangkan", "提取建议技能"],
  "2. Confirm before saving": ["2. Confirm before saving", "2. Sahkan sebelum menyimpan", "2. 保存前确认"],
  "AI cannot decide proficiency. Select only the suggested skills you actually know and choose your self-assessed level.": ["AI cannot decide proficiency. Select only the suggested skills you actually know and choose your self-assessed level.", "AI tidak boleh menentukan tahap penguasaan. Pilih kemahiran yang benar-benar anda kuasai dan tetapkan tahap penilaian kendiri.", "AI 无法判断熟练程度。请仅选择你确实掌握的建议技能，并选择自评等级。"],
  "Submit synthetic CV text to see suggested skills.": ["Submit synthetic CV text to see suggested skills.", "Hantar teks CV sintetik untuk melihat kemahiran yang dicadangkan.", "提交合成简历文本以查看建议技能。"],
  "Save confirmed skills to demo profile": ["Save confirmed skills to demo profile", "Simpan kemahiran yang disahkan ke profil demo", "将已确认的技能保存到演示档案"],
  "What this does—and doesn't do": ["What this does—and doesn't do", "Perkara yang dilakukan dan tidak dilakukan", "功能说明与限制"],
  "Does:": ["Does:", "Dilakukan:", "可以做到："],
  "request live extraction if configured, validate canonical skill IDs and exact CV excerpts, allow user verification, and save explicitly confirmed skills to the existing demo profile.": ["request live extraction if configured, validate canonical skill IDs and exact CV excerpts, allow user verification, and save explicitly confirmed skills to the existing demo profile.", "meminta pengekstrakan langsung jika dikonfigurasi, mengesahkan ID kemahiran kanonik dan petikan CV yang tepat, membolehkan pengesahan pengguna serta menyimpan kemahiran yang disahkan secara jelas ke profil demo sedia ada.", "在已配置时请求实时提取，验证规范技能 ID 和简历原文摘录，允许用户核实，并将明确确认的技能保存到现有演示档案。"],
  "Does not:": ["Does not:", "Tidak dilakukan:", "无法做到："],
  "authenticate users, store the CV body, run the original mockup career calculations through the backend, guarantee occupation outcomes, or prove a GPU is deployed until a live RunPod request succeeds.": ["authenticate users, store the CV body, run the original mockup career calculations through the backend, guarantee occupation outcomes, or prove a GPU is deployed until a live RunPod request succeeds.", "mengesahkan pengguna, menyimpan kandungan CV, menjalankan pengiraan kerjaya mockup asal melalui bahagian belakang, menjamin hasil pekerjaan atau membuktikan GPU telah digunakan sebelum permintaan RunPod langsung berjaya.", "验证用户身份、存储简历正文、通过后端运行原型中的职业计算、保证职业结果，或在实时 RunPod 请求成功前证明 GPU 已部署。"],
  "Checking backend configuration": ["Checking backend configuration", "Menyemak konfigurasi bahagian belakang", "正在检查后端配置"],
  "Extracting…": ["Extracting…", "Sedang mengekstrak…", "正在提取……"],
  "No grounded skill suggestions. You can continue using manual skill intake.": ["No grounded skill suggestions. You can continue using manual skill intake.", "Tiada cadangan kemahiran berasaskan bukti. Anda boleh meneruskan dengan memasukkan kemahiran secara manual.", "没有基于证据的技能建议。你可以继续手动填写技能。"],
  "Evidence:": ["Evidence:", "Bukti:", "依据："],
  "Submit synthetic CV text": ["Submit synthetic CV text", "Hantar teks CV sintetik", "提交合成简历文本"],
  "Save error:": ["Save error:", "Ralat simpan:", "保存错误："],
  "Provider:": ["Provider:", "Penyedia:", "服务商："],
  "configured": ["configured", "dikonfigurasi", "已配置"],
  "not configured": ["not configured", "tidak dikonfigurasi", "未配置"],
  "FuturePath · Live AI Skill Review": ["FuturePath · Live AI Skill Review", "FuturePath · Semakan Kemahiran AI Langsung", "FuturePath · 实时 AI 技能审核"],
  "Choose a PDF first.": ["Choose a PDF first.", "Pilih fail PDF dahulu.", "请先选择 PDF 文件。"],
  "Add at least one skill.": ["Add at least one skill.", "Tambah sekurang-kurangnya satu kemahiran.", "请至少添加一项技能。"],
  "Tick the box to confirm these skills describe you.": ["Tick the box to confirm these skills describe you.", "Tandakan kotak untuk mengesahkan kemahiran ini menggambarkan diri anda.", "请勾选方框，确认这些技能符合你的实际情况。"],
  "Could not delete:": ["Could not delete:", "Tidak dapat memadam:", "无法删除："],
  "My profile": ["My profile", "Profil saya", "我的档案"],
  "Choose a PDF": ["Choose a PDF", "Pilih PDF", "选择 PDF"],
  "Pick your skills from a list. Takes about 3 minutes.": ["Pick your skills from a list. Takes about 3 minutes.", "Pilih kemahiran anda daripada senarai. Proses ini mengambil masa kira-kira 3 minit.", "从列表中选择你的技能，约需 3 分钟。"],
  "Your PDF looked scanned, so Claude read the page images. Each skill quotes the text it came from; please check them carefully.": ["Your PDF looked scanned, so Claude read the page images. Each skill quotes the text it came from; please check them carefully.", "PDF anda kelihatan seperti imbasan, jadi Claude membaca imej halaman. Setiap kemahiran memetik teks sumbernya; sila semak dengan teliti.", "你的 PDF 看起来是扫描件，因此 Claude 读取了页面图像。每项技能都附有原文摘录，请仔细核对。"],
  "Skills suggested by Claude from your CV. Each one quotes the line it came from. Please check them.": ["Skills suggested by Claude from your CV. Each one quotes the line it came from. Please check them.", "Kemahiran yang dicadangkan oleh Claude daripada CV anda. Setiap kemahiran memetik baris sumbernya. Sila semak.", "Claude 根据你的简历提出了这些技能建议，每项均附有来源原文。请仔细核对。"],
  "Claude reviewed a PDF with little or no extractable text, and the local dictionary checked its transcription. Verify the suggested details, skills and evidence.": ["Claude reviewed a PDF with little or no extractable text, and the local dictionary checked its transcription. Verify the suggested details, skills and evidence.", "Claude menyemak PDF yang mempunyai sedikit atau tiada teks yang boleh diekstrak, dan kamus tempatan menyemak transkripsinya. Sahkan butiran, kemahiran dan bukti yang dicadangkan.", "Claude 审阅了一份几乎没有可提取文本的 PDF，本地词典核对了其转录内容。请核实建议的详情、技能和证据。"],
  "Claude and the local dictionary suggested skills from your CV. Review their evidence and choose each proficiency level.": ["Claude and the local dictionary suggested skills from your CV. Review their evidence and choose each proficiency level.", "Claude dan kamus tempatan mencadangkan kemahiran daripada CV anda. Semak buktinya dan pilih tahap kemahiran bagi setiap satu.", "Claude 和本地词典根据你的简历提出了技能建议。请核对证据，并为每项技能选择熟练程度。"],
  "Skills matched by the local dictionary, not GPU AI. Review every suggestion carefully.": ["Skills matched by the local dictionary, not GPU AI. Review every suggestion carefully.", "Kemahiran dipadankan oleh kamus tempatan, bukan AI GPU. Semak setiap cadangan dengan teliti.", "技能由本地词典匹配，而非 GPU AI。请仔细核对每项建议。"],
  "Extracting skills (GPU may be starting)…": ["Extracting skills (GPU may be starting)…", "Mengekstrak kemahiran (GPU mungkin sedang dimulakan)…", "正在提取技能（GPU 可能正在启动）…"],
  "Choose Basic, Working or Strong for every AI-suggested skill before continuing.": ["Choose Basic, Working or Strong for every AI-suggested skill before continuing.", "Pilih Asas, Boleh bekerja atau Mahir bagi setiap kemahiran yang dicadangkan AI sebelum meneruskan.", "继续之前，请为每项 AI 建议的技能选择基础、熟练应用或精通。"],
  "Details suggested from this CV — review before saving": ["Details suggested from this CV — review before saving", "Butiran yang dicadangkan daripada CV ini — semak sebelum menyimpan", "根据此简历建议的详情——保存前请核对"],
  "Review or edit the fields below. An in-progress degree is not a completed qualification. Projects, achievements and certifications are shown for review and are not automatically stored or scored.": ["Review or edit the fields below. An in-progress degree is not a completed qualification. Projects, achievements and certifications are shown for review and are not automatically stored or scored.", "Semak atau sunting medan di bawah. Ijazah yang masih dalam pengajian bukan kelayakan yang telah tamat. Projek, pencapaian dan pensijilan dipaparkan untuk semakan dan tidak disimpan atau diberi skor secara automatik.", "请核对或编辑以下字段。在读学位不等于已完成的学历。项目、成就和证书仅供核对，不会自动保存或计分。"],
  "This PDF has no readable text. Upload a text-based PDF, use the manual skills form, or configure Claude for scanned PDFs.": ["This PDF has no readable text. Upload a text-based PDF, use the manual skills form, or configure Claude for scanned PDFs.", "PDF ini tiada teks yang boleh dibaca. Muat naik PDF berasaskan teks, gunakan borang kemahiran manual, atau konfigurasikan Claude untuk PDF imbasan.", "此 PDF 没有可读取的文本。请上传文本型 PDF、使用手动技能表单，或为扫描版 PDF 配置 Claude。"],
  "Current role": ["Current role", "Jawatan semasa", "当前职位"],
  "Education (may be in progress)": ["Education (may be in progress)", "Pendidikan (mungkin masih dalam pengajian)", "教育背景（可能在读）"],
  "Highest completed qualification (confirm)": ["Highest completed qualification (confirm)", "Kelayakan tertinggi yang telah tamat (sahkan)", "已完成的最高学历（请确认）"],
  "keyword matching (no AI)": ["keyword matching (no AI)", "padanan kata kunci (tanpa AI)", "关键词匹配（未使用 AI）"],
  "Skills you added in the form. Set how strong each one is.": ["Skills you added in the form. Set how strong each one is.", "Kemahiran yang anda tambah dalam borang. Tetapkan tahap penguasaan bagi setiap kemahiran.", "你在表格中添加的技能。请为每项技能设置熟练程度。"],
  "These are the skills saved in your profile.": ["These are the skills saved in your profile.", "Ini ialah kemahiran yang disimpan dalam profil anda.", "这些是保存在你档案中的技能。"],
  "Add the skills you have.": ["Add the skills you have.", "Tambah kemahiran yang anda miliki.", "添加你具备的技能。"],
  "Fetching feeds and tagging new items… this can take a minute.": ["Fetching feeds and tagging new items… this can take a minute.", "Sedang mengambil suapan dan menandai item baharu… proses ini mungkin mengambil masa seminit.", "正在获取信息源并标注新条目……可能需要一分钟。"],
  "Refresh failed:": ["Refresh failed:", "Muat semula gagal:", "刷新失败："],
  "configuration is not a live health test": ["configuration is not a live health test", "konfigurasi bukan ujian kesihatan langsung", "配置状态不代表实时健康检查"],
  "Can support SDG 8 when data analysis helps organisations raise productivity and plan for decent, skilled jobs in Malaysia's growing digital economy.": ["Can support SDG 8 when data analysis helps organisations raise productivity and plan for decent, skilled jobs in Malaysia's growing digital economy.", "Boleh menyokong SDG 8 apabila analisis data membantu organisasi meningkatkan produktiviti dan merancang pekerjaan yang layak dan berkemahiran dalam ekonomi digital Malaysia yang semakin berkembang.", "当数据分析帮助机构提高生产力，并在马来西亚不断增长的数字经济中规划体面的技能型工作时，可支持可持续发展目标 8。"],
  "Supports SDG 9 by protecting the digital infrastructure that banks, hospitals and public services rely on, so innovation can grow on systems people trust.": ["Supports SDG 9 by protecting the digital infrastructure that banks, hospitals and public services rely on, so innovation can grow on systems people trust.", "Menyokong SDG 9 dengan melindungi infrastruktur digital yang menjadi sandaran bank, hospital dan perkhidmatan awam, supaya inovasi dapat berkembang di atas sistem yang dipercayai.", "通过保护银行、医院和公共服务所依赖的数字基础设施，支持可持续发展目标 9，让创新建立在人们信任的系统之上。"],
  "Can support SDG 8 when careful analysis channels investment to productive businesses and SMEs that sustain growth and jobs.": ["Can support SDG 8 when careful analysis channels investment to productive businesses and SMEs that sustain growth and jobs.", "Boleh menyokong SDG 8 apabila analisis yang teliti menyalurkan pelaburan kepada perniagaan dan PKS yang produktif, yang mengekalkan pertumbuhan dan pekerjaan.", "当审慎的分析将投资引向能够维持增长和就业的高生产力企业及中小企业时，可支持可持续发展目标 8。"],
  "Supports SDG 9 by turning operational data into dashboards and reports that help firms modernise processes and use their infrastructure better.": ["Supports SDG 9 by turning operational data into dashboards and reports that help firms modernise processes and use their infrastructure better.", "Menyokong SDG 9 dengan menukar data operasi kepada papan pemuka dan laporan yang membantu syarikat memodenkan proses dan menggunakan infrastruktur dengan lebih baik.", "通过将运营数据转化为仪表板和报告，帮助企业实现流程现代化并更好地利用基础设施，支持可持续发展目标 9。"],
  "Supports SDG 3 by keeping patient records accurate, secure and shared between hospitals, so clinicians can give safer and faster care.": ["Supports SDG 3 by keeping patient records accurate, secure and shared between hospitals, so clinicians can give safer and faster care.", "Menyokong SDG 3 dengan memastikan rekod pesakit tepat, selamat dan dikongsi antara hospital, supaya doktor dapat memberikan rawatan yang lebih selamat dan pantas.", "通过确保患者记录准确、安全并在医院之间共享，让医护人员提供更安全、更及时的护理，支持可持续发展目标 3。"],
  "Supports SDG 3 by running ethical, well-documented clinical trials that bring safe new treatments and medicines to patients.": ["Supports SDG 3 by running ethical, well-documented clinical trials that bring safe new treatments and medicines to patients.", "Menyokong SDG 3 dengan menjalankan ujian klinikal yang beretika dan didokumentasikan dengan baik, yang membawa rawatan dan ubat baharu yang selamat kepada pesakit.", "通过开展符合伦理、记录完善的临床试验，为患者带来安全的新疗法和新药物，支持可持续发展目标 3。"],
  "Supports SDG 12 and SDG 13 by measuring emissions and resource use and preparing sustainability reports that help companies cut waste and carbon.": ["Supports SDG 12 and SDG 13 by measuring emissions and resource use and preparing sustainability reports that help companies cut waste and carbon.", "Menyokong SDG 12 dan SDG 13 dengan mengukur pelepasan dan penggunaan sumber serta menyediakan laporan kemampanan yang membantu syarikat mengurangkan pembaziran dan karbon.", "通过测量排放和资源使用并编制可持续发展报告，帮助企业减少浪费和碳排放，支持可持续发展目标 12 和 13。"],
  "Supports SDG 7 and SDG 13 by designing solar, wind and battery systems that add clean, affordable power and cut emissions from electricity.": ["Supports SDG 7 and SDG 13 by designing solar, wind and battery systems that add clean, affordable power and cut emissions from electricity.", "Menyokong SDG 7 dan SDG 13 dengan mereka bentuk sistem solar, angin dan bateri yang menambah tenaga bersih dan mampu milik serta mengurangkan pelepasan daripada penjanaan elektrik.", "通过设计太阳能、风能和电池储能系统，增加清洁且负担得起的电力，并减少发电产生的排放，支持可持续发展目标 7 和 13。"],
  "Supports SDG 9 by upgrading factories with automation and control systems that raise productivity and keep manufacturing competitive.": ["Supports SDG 9 by upgrading factories with automation and control systems that raise productivity and keep manufacturing competitive.", "Menyokong SDG 9 dengan menaik taraf kilang menggunakan sistem automasi dan kawalan yang meningkatkan produktiviti dan mengekalkan daya saing pembuatan.", "通过以自动化和控制系统升级工厂，提高生产力并保持制造业竞争力，支持可持续发展目标 9。"],
  "Supports SDG 9 and SDG 12 by building reliable production processes that reduce defects, rework and scrap, so less material is wasted.": ["Supports SDG 9 and SDG 12 by building reliable production processes that reduce defects, rework and scrap, so less material is wasted.", "Menyokong SDG 9 dan SDG 12 dengan membina proses pengeluaran yang boleh dipercayai untuk mengurangkan kecacatan, kerja semula dan sisa, supaya kurang bahan dibazirkan.", "通过建立可靠的生产流程，减少缺陷、返工和废料，从而减少材料浪费，支持可持续发展目标 9 和 12。"],
  "Supports SDG 4 by designing clear, inclusive courses and digital learning that help more people learn and reskill throughout their lives.": ["Supports SDG 4 by designing clear, inclusive courses and digital learning that help more people learn and reskill throughout their lives.", "Menyokong SDG 4 dengan mereka bentuk kursus dan pembelajaran digital yang jelas dan inklusif, yang membantu lebih ramai orang belajar dan meningkatkan kemahiran sepanjang hayat.", "通过设计清晰、包容的课程和数字化学习，帮助更多人终身学习和再培训，支持可持续发展目标 4。"],
  "Supports SDG 10 by making digital services accessible and easy to use for people of different ages, abilities and languages, so fewer people are left out.": ["Supports SDG 10 by making digital services accessible and easy to use for people of different ages, abilities and languages, so fewer people are left out.", "Menyokong SDG 10 dengan menjadikan perkhidmatan digital mudah diakses dan digunakan oleh orang pelbagai umur, keupayaan dan bahasa, supaya kurang orang tertinggal.", "通过让不同年龄、能力和语言的人都能便捷地使用数字服务，减少被排除在外的人群，支持可持续发展目标 10。"],
  "Energy and electricity systems": ["Energy and electricity systems", "Sistem tenaga dan elektrik", "能源与电力系统"],
  "Renewable energy engineering": ["Renewable energy engineering", "Kejuruteraan tenaga boleh baharu", "可再生能源工程"],
  "Instructional content development": ["Instructional content development", "Pembangunan kandungan pengajaran", "教学内容开发"],
  "Build your skills profile": ["Build your skills profile", "Bina profil kemahiran anda", "建立你的技能档案"],
  "Choose how to start. You'll review and confirm everything before anything is saved.": ["Choose how to start. You'll review and confirm everything before anything is saved.", "Pilih cara untuk bermula. Anda akan menyemak dan mengesahkan semuanya sebelum sebarang maklumat disimpan.", "选择开始方式。在保存任何内容之前，你都可以检查并确认所有信息。"],
  "See results →": ["See results →", "Lihat keputusan →", "查看结果 →"],
  "Delete": ["Delete", "Padam", "删除"],
  "Yes, delete": ["Yes, delete", "Ya, padam", "确认删除"],
  "Cancel": ["Cancel", "Batal", "取消"],
  "How would you like to start?": ["How would you like to start?", "Bagaimanakah anda ingin bermula?", "你想如何开始？"],
  "Upload a CV": ["Upload a CV", "Muat naik CV", "上传简历"],
  "PDF, up to 2 MB. Skills are matched to our catalog for you to check.": ["PDF, up to 2 MB. Skills are matched to our catalog for you to check.", "PDF, sehingga 2 MB. Kemahiran dipadankan dengan katalog kami untuk anda semak.", "PDF，最大 2 MB。系统会将技能与目录匹配，供你检查。"],
  "PDF · max 2 MB": ["PDF · max 2 MB", "PDF · maksimum 2 MB", "PDF · 最大 2 MB"],
  "Back": ["Back", "Kembali", "返回"],
  "Fill a short form": ["Fill a short form", "Isi borang ringkas", "填写简短表格"],
  "Current Job Title": ["Current Job Title", "Jawatan Semasa", "当前职位"],
  "Years of Relevant Experience": ["Years of Relevant Experience", "Tahun Pengalaman Berkaitan", "相关工作年限"],
  "Education Level": ["Education Level", "Tahap Pendidikan", "教育程度"],
  "No formal qualification": ["No formal qualification", "Tiada kelayakan formal", "无正式学历"],
  "Primary School Achievement Test (UPSR)": ["Primary School Achievement Test (UPSR)", "Ujian Pencapaian Sekolah Rendah (UPSR)", "小学成绩测验（UPSR）"],
  "Lower Secondary Assessment (PT3)": ["Lower Secondary Assessment (PT3)", "Pentaksiran Tingkatan 3 (PT3)", "初中评估（PT3）"],
  "Malaysian Certificate of Education (SPM)": ["Malaysian Certificate of Education (SPM)", "Sijil Pelajaran Malaysia (SPM)", "马来西亚教育文凭（SPM）"],
  "Malaysian Skills Certificate (SKM)": ["Malaysian Skills Certificate (SKM)", "Sijil Kemahiran Malaysia (SKM)", "马来西亚技能证书（SKM）"],
  "Malaysian Vocational Certificate (SVM)": ["Malaysian Vocational Certificate (SVM)", "Sijil Vokasional Malaysia (SVM)", "马来西亚职业证书（SVM）"],
  "Malaysian Higher School Certificate (STPM)": ["Malaysian Higher School Certificate (STPM)", "Sijil Tinggi Persekolahan Malaysia (STPM)", "马来西亚高级教育文凭（STPM）"],
  "Malaysian Matriculation Certificate": ["Malaysian Matriculation Certificate", "Sijil Matrikulasi Malaysia", "马来西亚大学预科证书"],
  "Foundation / Matriculation / equivalent": ["Foundation / Matriculation / equivalent", "Asasi / Matrikulasi / setaraf", "大学预科 / 矩阵课程 / 同等学历"],
  "Certificate": ["Certificate", "Sijil", "证书"],
  "Diploma": ["Diploma", "Diploma", "文凭"],
  "Advanced Diploma": ["Advanced Diploma", "Diploma Lanjutan", "高级文凭"],
  "Bachelor's Degree": ["Bachelor's Degree", "Ijazah Sarjana Muda", "学士学位"],
  "Postgraduate Certificate / Diploma": ["Postgraduate Certificate / Diploma", "Sijil / Diploma Pascasiswazah", "研究生证书 / 文凭"],
  "Master's Degree": ["Master's Degree", "Ijazah Sarjana", "硕士学位"],
  "Doctoral Degree (PhD)": ["Doctoral Degree (PhD)", "Ijazah Kedoktoran (PhD)", "博士学位（PhD）"],
  "Other qualification / equivalent": ["Other qualification / equivalent", "Kelayakan lain / setaraf", "其他学历 / 同等学历"],
  "Current Industry": ["Current Industry", "Industri Semasa", "当前行业"],
  "Your Competencies & Skills": ["Your Competencies & Skills", "Kompetensi & Kemahiran Anda", "你的能力与技能"],
  "Future Areas of Interest (comma separated)": ["Future Areas of Interest (comma separated)", "Bidang Minat Masa Depan (pisahkan dengan koma)", "未来感兴趣的领域（用逗号分隔）"],
  "Quick Questionnaire": ["Quick Questionnaire", "Soal Selidik Ringkas", "快速问卷"],
  "How would you rate your current day-to-day comfort with generative AI tools (ChatGPT, Gemini, Copilot)?": ["How would you rate your current day-to-day comfort with generative AI tools (ChatGPT, Gemini, Copilot)?", "Bagaimanakah anda menilai keselesaan harian anda menggunakan alat AI generatif (ChatGPT, Gemini, Copilot)?", "你如何评价自己日常使用生成式 AI 工具（ChatGPT、Gemini、Copilot）的熟练程度？"],
  "Beginner — occasional awareness, minimal practical use": ["Beginner — occasional awareness, minimal practical use", "Pemula — hanya mengetahui secara umum, jarang menggunakannya", "入门 — 偶尔听说过，几乎没有实际使用"],
  "Intermediate — use occasionally for drafting or summarization": ["Intermediate — use occasionally for drafting or summarization", "Pertengahan — kadangkala digunakan untuk menulis draf atau membuat ringkasan", "中级 — 偶尔用于起草或总结"],
  "Confident — use daily for workflow scripting or prompt chaining": ["Confident — use daily for workflow scripting or prompt chaining", "Yakin — digunakan setiap hari untuk skrip aliran kerja atau rantaian prompt", "熟练 — 每天用于工作流脚本或提示词链"],
  "How many hours per week can you realistically commit to modular upskilling?": ["How many hours per week can you realistically commit to modular upskilling?", "Berapa jam seminggu yang realistik untuk anda luangkan bagi meningkatkan kemahiran secara modular?", "你每周实际能投入多少小时进行模块化技能提升？"],
  "3 hours/week": ["3 hours/week", "3 jam/minggu", "每周 3 小时"],
  "6 hours/week": ["6 hours/week", "6 jam/minggu", "每周 6 小时"],
  "10 hours/week": ["10 hours/week", "10 jam/minggu", "每周 10 小时"],
  "15 hours/week": ["15 hours/week", "15 jam/minggu", "每周 15 小时"],
  "What is your preferred operational work arrangement?": ["What is your preferred operational work arrangement?", "Apakah aturan kerja operasi pilihan anda?", "你偏好的运营工作安排是什么？"],
  "Hybrid": ["Hybrid", "Hibrid", "混合办公"],
  "Remote": ["Remote", "Jarak jauh", "远程"],
  "On-site": ["On-site", "Di lokasi", "现场办公"],
  "What is your primary career motivation right now?": ["What is your primary career motivation right now?", "Apakah motivasi kerjaya utama anda sekarang?", "你目前最主要的职业动机是什么？"],
  "Safeguard employment against repetitive clerical displacement": ["Safeguard employment against repetitive clerical displacement", "Melindungi pekerjaan daripada penggantian tugas perkeranian yang berulang", "避免工作被重复性文职自动化取代"],
  "Fast-track transition into high-growth green tech or AI governance": ["Fast-track transition into high-growth green tech or AI governance", "Mempercepat peralihan ke teknologi hijau yang berkembang pesat atau tadbir urus AI", "加速转向高速增长的绿色科技或 AI 治理领域"],
  "Upgrade salary potential with verified TVET / HRD Corp micro-credentials": ["Upgrade salary potential with verified TVET / HRD Corp micro-credentials", "Meningkatkan potensi gaji melalui mikro-kredensial TVET / HRD Corp yang disahkan", "通过经认证的 TVET / HRD Corp 微证书提升薪资潜力"],
  "Explore a different career direction": ["Explore a different career direction", "Meneroka hala tuju kerjaya yang berbeza", "探索不同的职业方向"],
  "Choose one": ["Choose one", "Pilih satu", "请选择"],
  "Your current or most recent role": ["Your current or most recent role", "Jawatan semasa atau terkini anda", "你目前或最近的职位"],
  "Years of work experience": ["Years of work experience", "Tahun pengalaman kerja", "工作年限"],
  "Highest qualification": ["Highest qualification", "Kelayakan tertinggi", "最高学历"],
  "Languages you can work in (comma separated)": ["Languages you can work in (comma separated)", "Bahasa yang boleh digunakan untuk bekerja (pisahkan dengan koma)", "你可以使用的工作语言（用逗号分隔）"],
  "Your skills": ["Your skills", "Kemahiran anda", "你的技能"],
  "Search and add every skill you have used at work, study or volunteering.": ["Search and add every skill you have used at work, study or volunteering.", "Cari dan tambah kemahiran yang pernah anda gunakan di tempat kerja, pengajian atau sukarelawan.", "搜索并添加你在工作、学习或志愿服务中用过的技能。"],
  "No skills yet. Add at least one.": ["No skills yet. Add at least one.", "Belum ada kemahiran. Tambah sekurang-kurangnya satu.", "目前没有技能。请至少添加一项。"],
  "No matching skill in our catalogue.": ["No matching skill in our catalogue.", "Tiada kemahiran sepadan dalam katalog kami.", "目录中没有匹配的技能。"],
  "Done": ["Done", "Selesai", "完成"],
  "What do you want from your next role? (optional)": ["What do you want from your next role? (optional)", "Apakah yang anda inginkan daripada jawatan seterusnya? (pilihan)", "你希望下一份工作带来什么？（选填）"],
  "Continue →": ["Continue →", "Teruskan →", "继续 →"],
  "Check your profile": ["Check your profile", "Semak profil anda", "检查你的档案"],
  "Edit anything that's wrong. Remove skills you don't have and add any that are missing.": ["Edit anything that's wrong. Remove skills you don't have and add any that are missing.", "Ubah maklumat yang salah. Buang kemahiran yang tiada dan tambah kemahiran yang tertinggal.", "请修改错误信息，删除你不具备的技能，并补充遗漏的技能。"],
  "Profile name (a nickname is fine)": ["Profile name (a nickname is fine)", "Nama profil (nama samaran juga boleh)", "档案名称（可以使用昵称）"],
  "Headline": ["Headline", "Tajuk profil", "个人简介标题"],
  "Hours per week you can study": ["Hours per week you can study", "Jam belajar setiap minggu", "每周可学习小时数"],
  "Years of relevant experience": ["Years of relevant experience", "Tahun pengalaman berkaitan", "相关工作年限"],
  "Remove": ["Remove", "Buang", "移除"],
  "I have checked these skills and they describe me.": ["I have checked these skills and they describe me.", "Saya telah menyemak kemahiran ini dan semuanya menggambarkan diri saya.", "我已检查这些技能，它们符合我的实际情况。"],
  "Continue to the interest quiz →": ["Continue to the interest quiz →", "Teruskan ke kuiz minat →", "继续进行兴趣测验 →"],
  "What do you enjoy? (optional)": ["What do you enjoy? (optional)", "Apakah yang anda gemari? (pilihan)", "你喜欢做什么？（选填）"],
  "Skip the quiz": ["Skip the quiz", "Langkau kuiz", "跳过测验"],
  "What happens next": ["What happens next", "Apa yang berlaku seterusnya", "接下来会发生什么"],
  "Your skills are scored against every career in the catalogue.": ["Your skills are scored against every career in the catalogue.", "Kemahiran anda dinilai berbanding setiap kerjaya dalam katalog.", "系统会将你的技能与目录中的每一个职业进行匹配评分。"],
  "Demand comes from dated, sourced trend signals.": ["Demand comes from dated, sourced trend signals.", "Permintaan dikira daripada isyarat trend bersumber dan bertarikh.", "需求依据有来源和日期的趋势信号计算。"],
  "You get a week-by-week plan with checked courses.": ["You get a week-by-week plan with checked courses.", "Anda akan mendapat pelan mingguan dengan kursus yang disemak.", "你将获得按周安排的学习计划及已核查课程。"],
  "🔒 Private by design": ["🔒 Private by design", "🔒 Privasi diutamakan", "🔒 以隐私为设计原则"],
  "Interest quiz": ["Interest quiz", "Kuiz minat", "兴趣测验"],
  "Compare full AI scenarios": ["Compare full AI scenarios", "Bandingkan senario AI sepenuhnya", "比较完整的 AI 情景"],
  "Priority": ["Priority", "Keutamaan", "优先级"],
  "Build:": ["Build:", "Bina:", "提升："],
  "Assess:": ["Assess:", "Nilai:", "评估："],
  "Learning priority from the current scenario": ["Learning priority from the current scenario", "Keutamaan pembelajaran daripada senario semasa", "当前情景下的学习优先项"],
  "Confirm proficiency before treating this as a gap": ["Confirm proficiency before treating this as a gap", "Sahkan tahap kemahiran sebelum menganggapnya sebagai jurang", "在将其视为技能差距前，请先确认熟练程度"],
  "Provider-page dates are shown for individually checked courses; imported entries show their catalogue snapshot date. Confirm current costs, hours and HRD Corp eligibility with the provider. Weeks assume your study hours per week.": ["Provider-page dates are shown for individually checked courses; imported entries show their catalogue snapshot date. Confirm current costs, hours and HRD Corp eligibility with the provider. Weeks assume your study hours per week.", "Tarikh halaman penyedia dipaparkan bagi kursus yang disemak secara individu; entri yang diimport memaparkan tarikh snapshot katalog. Sahkan kos, jam dan kelayakan HRD Corp dengan penyedia. Anggaran minggu berdasarkan jam belajar anda setiap minggu.", "单独核查的课程会显示提供方网页日期；导入条目显示目录快照日期。请向提供方确认当前费用、学时和 HRD Corp 资格。周数按你每周可学习的时间估算。"],
  "Potential alignment only; actual contribution depends on how work is carried out and its outcomes.": ["Potential alignment only; actual contribution depends on how work is carried out and its outcomes.", "Ini hanya potensi penjajaran; sumbangan sebenar bergantung pada cara kerja dilakukan dan hasilnya.", "这仅表示潜在关联；实际贡献取决于工作方式及其成果。"],
  "Source catalogue snapshot": ["Source catalogue snapshot", "Snapshot katalog sumber", "来源目录快照"],
  "Provider page checked": ["Provider page checked", "Halaman penyedia disemak", "已核查提供方网页"],
  "Verification date not recorded": ["Verification date not recorded", "Tarikh pengesahan tidak direkodkan", "未记录核查日期"],
  "Data Analyst": ["Data Analyst", "Penganalisis Data", "数据分析师"],
  "Cybersecurity Analyst": ["Cybersecurity Analyst", "Penganalisis Keselamatan Siber", "网络安全分析师"],
  "Financial Analyst": ["Financial Analyst", "Penganalisis Kewangan", "金融分析师"],
  "Business Intelligence Analyst": ["Business Intelligence Analyst", "Penganalisis Risikan Perniagaan", "商业智能分析师"],
  "Health Informatics Specialist": ["Health Informatics Specialist", "Pakar Informatik Kesihatan", "健康信息学专员"],
  "Clinical Research Coordinator": ["Clinical Research Coordinator", "Penyelaras Penyelidikan Klinikal", "临床研究协调员"],
  "Sustainability Analyst": ["Sustainability Analyst", "Penganalisis Kemampanan", "可持续发展分析师"],
  "Renewable Energy Engineer": ["Renewable Energy Engineer", "Jurutera Tenaga Boleh Baharu", "可再生能源工程师"],
  "Automation Engineer": ["Automation Engineer", "Jurutera Automasi", "自动化工程师"],
  "Quality Assurance Engineer": ["Quality Assurance Engineer", "Jurutera Jaminan Kualiti", "质量保证工程师"],
  "Instructional Designer": ["Instructional Designer", "Pereka Bentuk Pengajaran", "教学设计师"],
  "UX Designer": ["UX Designer", "Pereka Bentuk UX", "用户体验设计师"],
  "Good Health and Well-Being": ["Good Health and Well-Being", "Kesihatan Baik dan Kesejahteraan", "良好健康与福祉"],
  "Quality Education": ["Quality Education", "Pendidikan Berkualiti", "优质教育"],
  "Affordable and Clean Energy": ["Affordable and Clean Energy", "Tenaga Mampu Milik dan Bersih", "经济适用的清洁能源"],
  "Decent Work and Economic Growth": ["Decent Work and Economic Growth", "Pekerjaan Wajar dan Pertumbuhan Ekonomi", "体面工作和经济增长"],
  "Industry, Innovation and Infrastructure": ["Industry, Innovation and Infrastructure", "Industri, Inovasi dan Infrastruktur", "产业、创新和基础设施"],
  "Reduced Inequalities": ["Reduced Inequalities", "Mengurangkan Ketidaksamaan", "减少不平等"],
  "Responsible Consumption and Production": ["Responsible Consumption and Production", "Penggunaan dan Pengeluaran Bertanggungjawab", "负责任消费和生产"],
  "Responsible Consumption": ["Responsible Consumption", "Penggunaan Bertanggungjawab", "负责任消费"],
  "Climate Action": ["Climate Action", "Tindakan Iklim", "气候行动"],
  "No Poverty": ["No Poverty", "Tiada Kemiskinan", "无贫穷"],
  "Zero Hunger": ["Zero Hunger", "Sifar Kelaparan", "零饥饿"],
  "Good Health": ["Good Health", "Kesihatan Baik", "良好健康"],
  "Gender Equality": ["Gender Equality", "Kesaksamaan Gender", "性别平等"],
  "Clean Water": ["Clean Water", "Air Bersih", "清洁饮水"],
  "Clean Energy": ["Clean Energy", "Tenaga Bersih", "清洁能源"],
  "Decent Work": ["Decent Work", "Pekerjaan Wajar", "体面工作"],
  "Industry & Innovation": ["Industry & Innovation", "Industri & Inovasi", "产业与创新"],
  "Sustainable Cities": ["Sustainable Cities", "Bandar Mampan", "可持续城市"],
  "Life Below Water": ["Life Below Water", "Kehidupan di Bawah Air", "水下生物"],
  "Life on Land": ["Life on Land", "Kehidupan di Darat", "陆地生物"],
  "Peace & Justice": ["Peace & Justice", "Keamanan & Keadilan", "和平与正义"],
  "Partnerships": ["Partnerships", "Kerjasama", "促进目标实现的伙伴关系"],
  "SQL querying": ["SQL querying", "Pertanyaan SQL", "SQL 查询"],
  "Statistics": ["Statistics", "Statistik", "统计学"],
  "Data cleaning": ["Data cleaning", "Pembersihan data", "数据清理"],
  "Data visualisation": ["Data visualisation", "Visualisasi data", "数据可视化"],
  "Python programming": ["Python programming", "Pengaturcaraan Python", "Python 编程"],
  "Data modelling": ["Data modelling", "Pemodelan data", "数据建模"],
  "Communication": ["Communication", "Komunikasi", "沟通"],
  "Business analysis": ["Business analysis", "Analisis perniagaan", "业务分析"],
  "AI output validation": ["AI output validation", "Pengesahan output AI", "AI 输出验证"],
  "Network security": ["Network security", "Keselamatan rangkaian", "网络安全"],
  "Security fundamentals": ["Security fundamentals", "Asas keselamatan", "安全基础"],
  "Incident response": ["Incident response", "Tindak balas insiden", "事件响应"],
  "Threat analysis": ["Threat analysis", "Analisis ancaman", "威胁分析"],
  "SIEM operations": ["SIEM operations", "Operasi SIEM", "SIEM 运维"],
  "Scripting": ["Scripting", "Penulisan skrip", "脚本编写"],
  "Risk assessment": ["Risk assessment", "Penilaian risiko", "风险评估"],
  "AI security awareness": ["AI security awareness", "Kesedaran keselamatan AI", "AI 安全意识"],
  "Financial modelling": ["Financial modelling", "Pemodelan kewangan", "财务建模"],
  "Accounting fundamentals": ["Accounting fundamentals", "Asas perakaunan", "会计基础"],
  "Spreadsheet analysis": ["Spreadsheet analysis", "Analisis hamparan elektronik", "电子表格分析"],
  "Financial reporting": ["Financial reporting", "Pelaporan kewangan", "财务报告"],
  "Forecasting": ["Forecasting", "Ramalan", "预测"],
  "Financial regulation awareness": ["Financial regulation awareness", "Kesedaran peraturan kewangan", "金融法规意识"],
  "Stakeholder communication": ["Stakeholder communication", "Komunikasi pihak berkepentingan", "利益相关方沟通"],
  "Data warehousing": ["Data warehousing", "Pergudangan data", "数据仓库"],
  "ETL pipelines": ["ETL pipelines", "Saluran paip ETL", "ETL 数据管道"],
  "Dashboard design": ["Dashboard design", "Reka bentuk papan pemuka", "仪表板设计"],
  "KPI design": ["KPI design", "Reka bentuk KPI", "KPI 设计"],
  "Requirements gathering": ["Requirements gathering", "Pengumpulan keperluan", "需求收集"],
  "Health information systems": ["Health information systems", "Sistem maklumat kesihatan", "卫生信息系统"],
  "Health data governance": ["Health data governance", "Tadbir urus data kesihatan", "健康数据治理"],
  "Healthcare workflows": ["Healthcare workflows", "Aliran kerja penjagaan kesihatan", "医疗工作流程"],
  "Interoperability standards": ["Interoperability standards", "Piawaian kebolehoperasian", "互操作性标准"],
  "Data privacy": ["Data privacy", "Privasi data", "数据隐私"],
  "Clinical terminology": ["Clinical terminology", "Terminologi klinikal", "临床术语"],
  "Clinical research protocols": ["Clinical research protocols", "Protokol penyelidikan klinikal", "临床研究方案"],
  "Research ethics": ["Research ethics", "Etika penyelidikan", "研究伦理"],
  "Clinical documentation": ["Clinical documentation", "Dokumentasi klinikal", "临床文档"],
  "Research data management": ["Research data management", "Pengurusan data penyelidikan", "研究数据管理"],
  "Participant coordination": ["Participant coordination", "Penyelarasan peserta", "参与者协调"],
  "Good Clinical Practice": ["Good Clinical Practice", "Amalan Klinikal Baik", "药物临床试验质量管理规范"],
  "Study monitoring": ["Study monitoring", "Pemantauan kajian", "研究监查"],
  "Sustainability reporting": ["Sustainability reporting", "Pelaporan kemampanan", "可持续发展报告"],
  "Environmental metrics": ["Environmental metrics", "Metrik alam sekitar", "环境指标"],
  "Carbon accounting": ["Carbon accounting", "Perakaunan karbon", "碳核算"],
  "Environmental regulation awareness": ["Environmental regulation awareness", "Kesedaran peraturan alam sekitar", "环境法规意识"],
  "Lifecycle assessment": ["Lifecycle assessment", "Penilaian kitar hayat", "生命周期评估"],
  "Energy systems": ["Energy systems", "Sistem tenaga", "能源系统"],
  "Electrical engineering fundamentals": ["Electrical engineering fundamentals", "Asas kejuruteraan elektrik", "电气工程基础"],
  "Technical design": ["Technical design", "Reka bentuk teknikal", "技术设计"],
  "Energy simulation": ["Energy simulation", "Simulasi tenaga", "能源仿真"],
  "Grid integration": ["Grid integration", "Integrasi grid", "电网并网"],
  "Engineering safety": ["Engineering safety", "Keselamatan kejuruteraan", "工程安全"],
  "Control systems": ["Control systems", "Sistem kawalan", "控制系统"],
  "PLC programming": ["PLC programming", "Pengaturcaraan PLC", "PLC 编程"],
  "Industrial automation": ["Industrial automation", "Automasi industri", "工业自动化"],
  "Robotics fundamentals": ["Robotics fundamentals", "Asas robotik", "机器人基础"],
  "Equipment troubleshooting": ["Equipment troubleshooting", "Penyelesaian masalah peralatan", "设备故障排查"],
  "Quality management systems": ["Quality management systems", "Sistem pengurusan kualiti", "质量管理体系"],
  "Root cause analysis": ["Root cause analysis", "Analisis punca akar", "根本原因分析"],
  "Testing methodology": ["Testing methodology", "Metodologi pengujian", "测试方法"],
  "Statistical process control": ["Statistical process control", "Kawalan proses statistik", "统计过程控制"],
  "Process improvement": ["Process improvement", "Penambahbaikan proses", "流程改进"],
  "Inspection automation": ["Inspection automation", "Automasi pemeriksaan", "检测自动化"],
  "Learning design": ["Learning design", "Reka bentuk pembelajaran", "学习设计"],
  "Assessment design": ["Assessment design", "Reka bentuk penilaian", "评估设计"],
  "Content development": ["Content development", "Pembangunan kandungan", "内容开发"],
  "Learning technologies": ["Learning technologies", "Teknologi pembelajaran", "学习技术"],
  "Accessibility design": ["Accessibility design", "Reka bentuk kebolehcapaian", "无障碍设计"],
  "Learning analytics": ["Learning analytics", "Analitik pembelajaran", "学习分析"],
  "User research": ["User research", "Penyelidikan pengguna", "用户研究"],
  "Interaction design": ["Interaction design", "Reka bentuk interaksi", "交互设计"],
  "Prototyping": ["Prototyping", "Prototaip", "原型设计"],
  "Usability testing": ["Usability testing", "Pengujian kebolehgunaan", "可用性测试"],
  "Information architecture": ["Information architecture", "Seni bina maklumat", "信息架构"],
  "Visual design": ["Visual design", "Reka bentuk visual", "视觉设计"],
  "AI literacy": ["AI literacy", "Literasi AI", "AI 素养"],
  "Project management": ["Project management", "Pengurusan projek", "项目管理"],
  "Leadership": ["Leadership", "Kepimpinan", "领导力"],
  "Teamwork": ["Teamwork", "Kerja berpasukan", "团队合作"],
  "Event management": ["Event management", "Pengurusan acara", "活动管理"],
  "Problem solving": ["Problem solving", "Penyelesaian masalah", "问题解决"],
  "THE EVIDENCE": ["THE EVIDENCE", "BUKTI", "证据"],
  "Data entry clerks": ["Data entry clerks", "Kerani kemasukan data", "数据录入文员"],
  "Accounting, bookkeeping and payroll clerks": ["Accounting, bookkeeping and payroll clerks", "Kerani perakaunan, simpan kira dan gaji", "会计、簿记和薪资文员"],
  "Administrative assistants and secretaries": ["Administrative assistants and secretaries", "Pembantu pentadbiran dan setiausaha", "行政助理和秘书"],
  "Bank tellers": ["Bank tellers", "Juruwang bank", "银行柜员"],
  "Postal service clerks": ["Postal service clerks", "Kerani perkhidmatan pos", "邮政服务文员"],
  "Cashiers and ticket clerks": ["Cashiers and ticket clerks", "Juruwang dan kerani tiket", "收银员和售票员"],
  "Customer service and client information workers": ["Customer service and client information workers", "Pekerja khidmat pelanggan dan maklumat pelanggan", "客户服务和客户信息人员"],
  "SKILL TRENDS": ["SKILL TRENDS", "TREND KEMAHIRAN", "技能趋势"],
  "Which skills are rising, and which are declining": ["Which skills are rising, and which are declining", "Kemahiran mana yang meningkat, dan mana yang semakin berkurang", "哪些技能在上升，哪些在减少"],
  "Counted from the dated signals listed below. The line shows each item's signals over the last 3 years; the badge counts them. Declining also includes jobs that WEF and ILO reports name as declining.": ["Counted from the dated signals listed below. The line shows each item's signals over the last 3 years; the badge counts them. Declining also includes jobs that WEF and ILO reports name as declining.", "Dikira daripada isyarat bertarikh yang disenaraikan di bawah. Garis menunjukkan isyarat setiap item dalam 3 tahun lepas; lencana mengiranya. Bahagian menurun juga termasuk pekerjaan yang dinyatakan semakin berkurang dalam laporan WEF dan ILO.", "根据下方列出的带日期信号统计。折线显示每项在过去 3 年的信号，徽章显示信号数量。“减少”一栏也包括 WEF 和 ILO 报告指出正在减少的职业。"],
  "Loading skill trends…": ["Loading skill trends…", "Memuatkan trend kemahiran…", "正在加载技能趋势…"],
  "Rising skills": ["Rising skills", "Kemahiran meningkat", "上升的技能"],
  "Declining skills & jobs": ["Declining skills & jobs", "Kemahiran & pekerjaan menurun", "减少的技能和职业"],
  "Net rising signals": ["Net rising signals", "Isyarat bersih meningkat", "净上升信号"],
  "Named as declining": ["Named as declining", "Dinyatakan menurun", "被列为减少"],
  "Show all": ["Show all", "Tunjuk semua", "显示全部"],
  "Show fewer": ["Show fewer", "Tunjuk kurang", "显示较少"],
  "See less": ["See less", "Lihat kurang", "收起"],
  "The signals behind these trends": ["The signals behind these trends", "Isyarat di sebalik trend ini", "这些趋势背后的信号"],
  "Declining job": ["Declining job", "Pekerjaan menurun", "减少的职业"],
  "Technical": ["Technical", "Teknikal", "技术"],
  "Analytical": ["Analytical", "Analitikal", "分析"],
  "Domain knowledge": ["Domain knowledge", "Pengetahuan bidang", "领域知识"],
  "Transferable": ["Transferable", "Boleh dipindah", "通用技能"],
  "Skill trends": ["Skill trends", "Trend kemahiran", "技能趋势"],
  "Mark as completed": ["Mark as completed", "Tanda selesai", "标记为已完成"],
  "✓ Completed": ["✓ Completed", "✓ Selesai", "✓ 已完成"],
  "ABOUT FUTUREPATH": ["ABOUT FUTUREPATH", "TENTANG FUTUREPATH", "关于 FUTUREPATH"],
  "THE PROBLEM": ["THE PROBLEM", "MASALAHNYA", "问题"],
  "HOW FUTUREPATH SOLVES IT": ["HOW FUTUREPATH SOLVES IT", "BAGAIMANA FUTUREPATH MENYELESAIKANNYA", "FUTUREPATH 如何解决"],
  "HOW WE USE AI": ["HOW WE USE AI", "CARA KAMI MENGGUNAKAN AI", "我们如何使用 AI"],
  "Helping Malaysians": ["Helping Malaysians", "Membantu rakyat Malaysia", "帮助马来西亚人"],
  "reskill for the AI era.": ["reskill for the AI era.", "melatih semula kemahiran untuk era AI.", "为 AI 时代重新掌握技能。"],
  "FuturePath is a career navigator for students, graduates, workers facing restructuring and career switchers. It shows which future-ready careers fit your skills, why, and how to get there with free or low-cost learning.": ["FuturePath is a career navigator for students, graduates, workers facing restructuring and career switchers. It shows which future-ready careers fit your skills, why, and how to get there with free or low-cost learning.", "FuturePath ialah panduan kerjaya untuk pelajar, graduan, pekerja yang menghadapi penstrukturan semula dan mereka yang bertukar kerjaya. Ia menunjukkan kerjaya masa depan yang sesuai dengan kemahiran anda, sebabnya, dan cara mencapainya melalui pembelajaran percuma atau kos rendah.", "FuturePath 是为学生、毕业生、面临重组的员工和转行者打造的职业导航工具。它展示哪些面向未来的职业适合你的技能、原因，以及如何通过免费或低成本学习实现目标。"],
  "Work is changing, and people are left guessing": ["Work is changing, and people are left guessing", "Pekerjaan sedang berubah, dan ramai dibiarkan meneka", "工作在变化，人们却只能猜测"],
  "From your CV to a plan you can act on": ["From your CV to a plan you can act on", "Daripada CV anda kepada pelan yang boleh dilaksanakan", "从你的简历到可执行的计划"],
  "Jobs are changing faster than people can retrain": ["Jobs are changing faster than people can retrain", "Pekerjaan berubah lebih pantas daripada orang boleh berlatih semula", "工作变化快于人们重新培训的速度"],
  "AI and automation are reshaping work in Malaysia. MOSTI expects more than 600,000 workers to need reskilling within 3 to 5 years, and clerical roles such as data entry and bookkeeping are declining fastest.": ["AI and automation are reshaping work in Malaysia. MOSTI expects more than 600,000 workers to need reskilling within 3 to 5 years, and clerical roles such as data entry and bookkeeping are declining fastest.", "AI dan automasi sedang mengubah pekerjaan di Malaysia. MOSTI menjangka lebih 600,000 pekerja perlu dilatih semula dalam 3 hingga 5 tahun, dan peranan perkeranian seperti kemasukan data dan simpan kira paling pantas berkurang.", "AI 和自动化正在重塑马来西亚的工作。MOSTI 预计未来 3 至 5 年内超过 60 万名员工需要重新培训，而数据录入、簿记等文书岗位减少得最快。"],
  "People use AI, but few are trained for it": ["People use AI, but few are trained for it", "Ramai menggunakan AI, tetapi sedikit yang terlatih", "人们在使用 AI，却很少受过培训"],
  "56% of Malaysian professionals use AI at work, yet only 26% have had formal training (Hays Asia Salary Guide 2025). Most don't know which of their skills still matter.": ["56% of Malaysian professionals use AI at work, yet only 26% have had formal training (Hays Asia Salary Guide 2025). Most don't know which of their skills still matter.", "56% profesional Malaysia menggunakan AI di tempat kerja, namun hanya 26% pernah menerima latihan formal (Hays Asia Salary Guide 2025). Kebanyakan tidak tahu kemahiran mana yang masih penting.", "56% 的马来西亚专业人士在工作中使用 AI，但只有 26% 接受过正式培训（Hays Asia Salary Guide 2025）。大多数人不知道自己的哪些技能仍然重要。"],
  "Career advice is generic and hard to trust": ["Career advice is generic and hard to trust", "Nasihat kerjaya bersifat umum dan sukar dipercayai", "职业建议笼统且难以信任"],
  "Job sites list vacancies, not a path from where you are now. Advice rarely shows its evidence, its date, or how it reached its answer, and paid courses put people off.": ["Job sites list vacancies, not a path from where you are now. Advice rarely shows its evidence, its date, or how it reached its answer, and paid courses put people off.", "Laman kerja menyenaraikan kekosongan, bukan laluan dari kedudukan anda sekarang. Nasihat jarang menunjukkan bukti, tarikh, atau cara jawapannya diperoleh, dan kursus berbayar menghalang ramai orang.", "招聘网站只列出空缺，而不是从你现在的位置出发的路径。建议很少说明证据、日期或得出结论的方法，而付费课程也让人望而却步。"],
  "Read your real skills": ["Read your real skills", "Membaca kemahiran sebenar anda", "读取你的真实技能"],
  "Upload a CV or fill a short form. Claude picks out skills, each with a quote from your CV, and you confirm every one.": ["Upload a CV or fill a short form. Claude picks out skills, each with a quote from your CV, and you confirm every one.", "Muat naik CV atau isi borang ringkas. Claude mengenal pasti kemahiran, setiap satu dengan petikan daripada CV anda, dan anda mengesahkan setiap satu.", "上传简历或填写简短表格。Claude 找出技能，每项都引用你简历中的原文，并由你逐一确认。"],
  "Match you to future careers": ["Match you to future careers", "Memadankan anda dengan kerjaya masa depan", "为你匹配未来职业"],
  "Careers are ranked by a visible formula: your skills, market demand from dated signals, and optional interest fit. You see each skills gap.": ["Careers are ranked by a visible formula: your skills, market demand from dated signals, and optional interest fit. You see each skills gap.", "Kerjaya disusun mengikut formula yang jelas: kemahiran anda, permintaan pasaran daripada isyarat bertarikh, dan kesesuaian minat (pilihan). Anda melihat setiap jurang kemahiran.", "职业按公开的公式排序：你的技能、来自带日期信号的市场需求，以及可选的兴趣匹配。你可以看到每项技能差距。"],
  "Show the evidence": ["Show the evidence", "Menunjukkan bukti", "展示证据"],
  "Every demand score comes from dated, sourced reports, news and research, refreshed daily: which skills are rising and which jobs are declining.": ["Every demand score comes from dated, sourced reports, news and research, refreshed daily: which skills are rising and which jobs are declining.", "Setiap skor permintaan datang daripada laporan, berita dan penyelidikan bertarikh dan bersumber, dikemas kini setiap hari: kemahiran mana yang meningkat dan pekerjaan mana yang berkurang.", "每个需求分数都来自带日期和来源的报告、新闻和研究，每天更新：哪些技能在上升，哪些职业在减少。"],
  "Plan an affordable route": ["Plan an affordable route", "Merancang laluan mampu milik", "规划负担得起的路线"],
  "An ordered learning plan using checked free, low-cost and HRD Corp-claimable courses, with hours, weeks and a tick-off progress tracker.": ["An ordered learning plan using checked free, low-cost and HRD Corp-claimable courses, with hours, weeks and a tick-off progress tracker.", "Pelan pembelajaran tersusun menggunakan kursus percuma, kos rendah dan boleh dituntut HRD Corp yang telah disemak, dengan jam, minggu dan penjejak kemajuan.", "按顺序排列的学习计划，使用经核查的免费、低成本和可申请 HRD Corp 的课程，并显示小时数、周数和可勾选的进度。"],
  "Be honest about uncertainty": ["Be honest about uncertainty", "Jujur tentang ketidakpastian", "坦诚面对不确定性"],
  "Moderate and Fast AI disruption scenarios show how the picture could change. Results are estimates, not predictions.": ["Moderate and Fast AI disruption scenarios show how the picture could change. Results are estimates, not predictions.", "Senario gangguan AI Sederhana dan Pantas menunjukkan bagaimana keadaan boleh berubah. Keputusan ialah anggaran, bukan ramalan.", "温和与快速 AI 冲击两种情景展示情况可能如何变化。结果是估计，而非预测。"],
  "Scenarios": ["Scenarios", "Senario", "情景"],
  "01 · Start": ["01 · Start", "01 · Mula", "01 · 开始"],
  "02 · Results": ["02 · Results", "02 · Keputusan", "02 · 结果"],
  "03 · Signals": ["03 · Signals", "03 · Isyarat", "03 · 信号"],
  "04 · Pathway": ["04 · Pathway", "04 · Laluan", "04 · 路径"],
  "05 · Scenarios": ["05 · Scenarios", "05 · Senario", "05 · 情景"],
  "hours left": ["hours left", "jam lagi", "小时剩余"],
  "weeks left": ["weeks left", "minggu lagi", "周剩余"],
};

const FP_SKILL_SDG_TEXT = {
  "Can support SDG 9 when software development skills help build and maintain reliable digital products and services.": ["Boleh menyokong SDG 9 apabila kemahiran pembangunan perisian membantu membina dan menyelenggara produk serta perkhidmatan digital yang boleh dipercayai.","当软件开发技能帮助构建和维护可靠的数字产品与服务时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when practical embedded and connected-system prototyping helps develop useful technology.": ["Boleh menyokong SDG 9 apabila prototaip sistem terbenam dan bersambung membantu membangunkan teknologi yang berguna.","当嵌入式与互联系统的实际原型开发推动实用技术发展时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when reliable queries help build or improve data systems used for industry, research, or public services.": ["Boleh menyokong SDG 9 apabila pertanyaan yang boleh dipercayai membantu membina atau menambah baik sistem data untuk industri, penyelidikan atau perkhidmatan awam.", "当可靠的查询有助于构建或改进用于工业、研究或公共服务的数据系统时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when sound statistical analysis informs evidence-based research, technology, or infrastructure decisions.": ["Boleh menyokong SDG 9 apabila analisis statistik yang kukuh memaklumkan keputusan berasaskan bukti dalam penyelidikan, teknologi atau infrastruktur.", "当严谨的统计分析为研究、技术或基础设施决策提供循证依据时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when accurate, well-prepared data improves the reliability of digital systems and analysis.": ["Boleh menyokong SDG 9 apabila data yang tepat dan disediakan dengan baik meningkatkan kebolehpercayaan sistem digital dan analisis.", "当准确且经过妥善处理的数据提高数字系统和分析的可靠性时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when clear visualisations help people understand evidence used to improve systems or services.": ["Boleh menyokong SDG 9 apabila visualisasi yang jelas membantu orang memahami bukti untuk menambah baik sistem atau perkhidmatan.", "当清晰的可视化帮助人们理解用于改进系统或服务的证据时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when software built with Python contributes to useful, reliable technological innovation.": ["Boleh menyokong SDG 9 apabila perisian yang dibina dengan Python menyumbang kepada inovasi teknologi yang berguna dan boleh dipercayai.", "当使用 Python 开发的软件推动实用且可靠的技术创新时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when well-designed data models enable reliable information systems and analysis.": ["Boleh menyokong SDG 9 apabila model data yang direka dengan baik membolehkan sistem maklumat dan analisis yang boleh dipercayai.", "当设计良好的数据模型支持可靠的信息系统和分析时，可支持可持续发展目标 9。"],
  "Can support SDG 8 when clear communication helps people collaborate, make informed decisions, and participate effectively at work.": ["Boleh menyokong SDG 8 apabila komunikasi yang jelas membantu orang bekerjasama, membuat keputusan termaklum dan mengambil bahagian dengan berkesan di tempat kerja.", "当清晰的沟通帮助人们协作、作出知情决策并有效参与工作时，可支持可持续发展目标 8。"],
  "Can support SDG 8 through better-informed work and SDG 9 when analysis helps organisations improve useful systems or processes.": ["Boleh menyokong SDG 8 melalui kerja yang lebih bermaklumat, serta SDG 9 apabila analisis membantu organisasi menambah baik sistem atau proses yang berguna.", "可通过提升工作的知情程度支持可持续发展目标 8；当分析帮助组织改进实用系统或流程时，也可支持目标 9。"],
  "Can support SDG 9 when checking AI outputs helps make technology more reliable, accountable, and useful.": ["Boleh menyokong SDG 9 apabila semakan output AI membantu menjadikan teknologi lebih boleh dipercayai, bertanggungjawab dan berguna.", "当检查 AI 输出有助于提升技术的可靠性、问责性和实用性时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when protecting networks improves the security and reliability of digital infrastructure.": ["Boleh menyokong SDG 9 apabila perlindungan rangkaian meningkatkan keselamatan dan kebolehpercayaan infrastruktur digital.", "当保护网络提升数字基础设施的安全性和可靠性时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when security fundamentals help maintain dependable digital systems and infrastructure.": ["Boleh menyokong SDG 9 apabila asas keselamatan membantu mengekalkan sistem dan infrastruktur digital yang boleh diharap.", "当安全基础知识有助于维护可靠的数字系统和基础设施时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when timely incident response restores the security and reliability of digital infrastructure.": ["Boleh menyokong SDG 9 apabila tindak balas insiden yang tepat pada masanya memulihkan keselamatan dan kebolehpercayaan infrastruktur digital.", "当及时的事件响应恢复数字基础设施的安全性和可靠性时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when threat analysis helps protect technology systems and the services that depend on them.": ["Boleh menyokong SDG 9 apabila analisis ancaman membantu melindungi sistem teknologi dan perkhidmatan yang bergantung padanya.", "当威胁分析帮助保护技术系统及依赖这些系统的服务时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when SIEM operations help detect threats and maintain reliable digital infrastructure.": ["Boleh menyokong SDG 9 apabila operasi SIEM membantu mengesan ancaman dan mengekalkan infrastruktur digital yang boleh dipercayai.", "当 SIEM 运维帮助发现威胁并维护可靠的数字基础设施时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when scripts automate or strengthen useful, maintainable digital systems.": ["Boleh menyokong SDG 9 apabila skrip mengautomasi atau memperkukuh sistem digital yang berguna dan mudah diselenggara.", "当脚本自动化或强化实用且易于维护的数字系统时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when risk assessment helps identify and reduce risks to technology, infrastructure, or service delivery.": ["Boleh menyokong SDG 9 apabila penilaian risiko membantu mengenal pasti dan mengurangkan risiko terhadap teknologi, infrastruktur atau penyampaian perkhidmatan.", "当风险评估帮助识别并降低技术、基础设施或服务交付方面的风险时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when awareness of AI security risks informs safer design and use of digital technologies.": ["Boleh menyokong SDG 9 apabila kesedaran tentang risiko keselamatan AI memaklumkan reka bentuk dan penggunaan teknologi digital yang lebih selamat.", "当对 AI 安全风险的认识促进数字技术更安全的设计与使用时，可支持可持续发展目标 9。"],
  "Can support SDG 8 when responsible financial models help organisations assess performance and make informed economic decisions.": ["Boleh menyokong SDG 8 apabila model kewangan yang bertanggungjawab membantu organisasi menilai prestasi dan membuat keputusan ekonomi termaklum.", "当负责任的财务模型帮助组织评估绩效并作出知情的经济决策时，可支持可持续发展目标 8。"],
  "Can support SDG 8 through trustworthy financial records and SDG 12 when accounting helps organisations understand resource use and obligations.": ["Boleh menyokong SDG 8 melalui rekod kewangan yang boleh dipercayai, serta SDG 12 apabila perakaunan membantu organisasi memahami penggunaan sumber dan tanggungjawab.", "可通过可信的财务记录支持可持续发展目标 8；当会计帮助组织了解资源使用和责任时，也可支持目标 12。"],
  "Can support SDG 8 when accurate spreadsheet analysis helps people make informed workplace and financial decisions.": ["Boleh menyokong SDG 8 apabila analisis hamparan elektronik yang tepat membantu orang membuat keputusan kerja dan kewangan secara termaklum.", "当准确的电子表格分析帮助人们作出知情的工作和财务决策时，可支持可持续发展目标 8。"],
  "Can support SDG 8 when transparent financial reporting supports accountability and informed economic decisions.": ["Boleh menyokong SDG 8 apabila pelaporan kewangan yang telus menyokong akauntabiliti dan keputusan ekonomi termaklum.", "当透明的财务报告促进问责并支持知情的经济决策时，可支持可持续发展目标 8。"],
  "Can support SDG 8 through better-informed planning and SDG 9 when forecasts help organisations plan investment in systems or innovation.": ["Boleh menyokong SDG 8 melalui perancangan yang lebih bermaklumat, serta SDG 9 apabila ramalan membantu organisasi merancang pelaburan dalam sistem atau inovasi.", "可通过提升规划的知情程度支持可持续发展目标 8；当预测帮助组织规划系统或创新投资时，也可支持目标 9。"],
  "Can support SDG 8 when understanding financial regulation helps organisations make responsible, compliant decisions.": ["Boleh menyokong SDG 8 apabila pemahaman tentang peraturan kewangan membantu organisasi membuat keputusan yang bertanggungjawab dan patuh.", "当理解金融法规帮助组织作出负责任且合规的决策时，可支持可持续发展目标 8。"],
  "Can support SDG 8 when constructive stakeholder communication enables informed, collaborative workplace decisions.": ["Boleh menyokong SDG 8 apabila komunikasi yang membina dengan pihak berkepentingan membolehkan keputusan tempat kerja dibuat secara termaklum dan bersama.", "当与利益相关方的建设性沟通促成知情且协作的工作决策时，可支持可持续发展目标 8。"],
  "Can support SDG 9 when a reliable data warehouse provides a sound foundation for analysis and digital services.": ["Boleh menyokong SDG 9 apabila gudang data yang boleh dipercayai menyediakan asas kukuh untuk analisis dan perkhidmatan digital.", "当可靠的数据仓库为分析和数字服务提供坚实基础时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when dependable data pipelines connect information needed for research, services, or innovation.": ["Boleh menyokong SDG 9 apabila saluran paip data yang boleh diharap menghubungkan maklumat yang diperlukan untuk penyelidikan, perkhidmatan atau inovasi.", "当可靠的数据管道连接研究、服务或创新所需的信息时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when useful dashboards make operational evidence accessible for improving systems and services.": ["Boleh menyokong SDG 9 apabila papan pemuka yang berguna memudahkan akses kepada bukti operasi untuk menambah baik sistem dan perkhidmatan.", "当实用的仪表板让人们能够获取运营证据以改进系统和服务时，可支持可持续发展目标 9。"],
  "Can support SDG 8 when meaningful measures inform work and organisational decisions, and SDG 9 when they track system improvement.": ["Boleh menyokong SDG 8 apabila ukuran yang bermakna memaklumkan keputusan kerja dan organisasi, serta SDG 9 apabila ukuran itu menjejaki penambahbaikan sistem.", "当有意义的指标为工作和组织决策提供依据时，可支持可持续发展目标 8；当其追踪系统改进时，也可支持目标 9。"],
  "Can support SDG 9 when carefully gathered requirements help teams build technology that addresses real user and service needs.": ["Boleh menyokong SDG 9 apabila keperluan yang dikumpulkan dengan teliti membantu pasukan membina teknologi yang memenuhi keperluan sebenar pengguna dan perkhidmatan.", "当经过仔细收集的需求帮助团队开发满足用户和服务实际需要的技术时，可支持可持续发展目标 9。"],
  "Can support SDG 3 when health information systems help care teams access and manage information for health services.": ["Boleh menyokong SDG 3 apabila sistem maklumat kesihatan membantu pasukan penjagaan mengakses dan mengurus maklumat untuk perkhidmatan kesihatan.", "当卫生信息系统帮助医疗团队获取和管理卫生服务所需信息时，可支持可持续发展目标 3。"],
  "Can support SDG 3 when responsible health-data governance helps protect information and support trustworthy health services.": ["Boleh menyokong SDG 3 apabila tadbir urus data kesihatan yang bertanggungjawab melindungi maklumat dan menyokong perkhidmatan kesihatan yang boleh dipercayai.", "当负责任的健康数据治理保护信息并支持可信赖的卫生服务时，可支持可持续发展目标 3。"],
  "Can support SDG 3 when understanding healthcare workflows helps improve the coordination and delivery of health services.": ["Boleh menyokong SDG 3 apabila pemahaman tentang aliran kerja penjagaan kesihatan membantu meningkatkan penyelarasan dan penyampaian perkhidmatan kesihatan.", "当理解医疗工作流程有助于改善卫生服务的协调与提供时，可支持可持续发展目标 3。"],
  "Can support SDG 3 when health systems exchange information safely, and SDG 9 when interoperability strengthens digital infrastructure.": ["Boleh menyokong SDG 3 apabila sistem kesihatan bertukar maklumat dengan selamat, serta SDG 9 apabila kebolehoperasian memperkukuh infrastruktur digital.", "当卫生系统安全地交换信息时，可支持可持续发展目标 3；当互操作性强化数字基础设施时，也可支持目标 9。"],
  "Can support SDG 3 when privacy practices protect sensitive health information and help maintain trust in health services.": ["Boleh menyokong SDG 3 apabila amalan privasi melindungi maklumat kesihatan yang sensitif dan membantu mengekalkan kepercayaan terhadap perkhidmatan kesihatan.", "当隐私实践保护敏感健康信息并帮助维持人们对卫生服务的信任时，可支持可持续发展目标 3。"],
  "Can support SDG 3 when consistent clinical terminology helps health professionals interpret and exchange patient information.": ["Boleh menyokong SDG 3 apabila istilah klinikal yang konsisten membantu profesional kesihatan mentafsir dan bertukar maklumat pesakit.", "当一致的临床术语帮助卫生专业人员解读和交换患者信息时，可支持可持续发展目标 3。"],
  "Can support SDG 3 when sound research protocols help produce ethical, reliable evidence relevant to health.": ["Boleh menyokong SDG 3 apabila protokol penyelidikan yang kukuh membantu menghasilkan bukti kesihatan yang beretika dan boleh dipercayai.", "当严谨的研究方案有助于产出符合伦理且可靠的健康相关证据时，可支持可持续发展目标 3。"],
  "Can support SDG 3 when research ethics protects participants and supports trustworthy health research.": ["Boleh menyokong SDG 3 apabila etika penyelidikan melindungi peserta dan menyokong penyelidikan kesihatan yang boleh dipercayai.", "当研究伦理保护参与者并支持可信赖的健康研究时，可支持可持续发展目标 3。"],
  "Can support SDG 3 when accurate clinical documentation supports continuity, safety, and accountability in care.": ["Boleh menyokong SDG 3 apabila dokumentasi klinikal yang tepat menyokong kesinambungan, keselamatan dan akauntabiliti penjagaan.", "当准确的临床文档支持护理的连续性、安全性和问责时，可支持可持续发展目标 3。"],
  "Can support SDG 3 when well-managed research data improves the integrity and reusability of health evidence.": ["Boleh menyokong SDG 3 apabila data penyelidikan yang diurus dengan baik meningkatkan integriti dan kebolehgunaan semula bukti kesihatan.", "当妥善管理的研究数据提高健康证据的完整性和可复用性时，可支持可持续发展目标 3。"],
  "Can support SDG 3 when respectful participant coordination helps people take part safely in health research.": ["Boleh menyokong SDG 3 apabila penyelarasan peserta yang menghormati mereka membantu orang menyertai penyelidikan kesihatan dengan selamat.", "当尊重参与者的协调工作帮助人们安全参与健康研究时，可支持可持续发展目标 3。"],
  "Can support SDG 3 when Good Clinical Practice is applied to protect participants and support reliable clinical research.": ["Boleh menyokong SDG 3 apabila Amalan Klinikal Baik digunakan untuk melindungi peserta dan menyokong penyelidikan klinikal yang boleh dipercayai.", "当实施药物临床试验质量管理规范以保护参与者并支持可靠的临床研究时，可支持可持续发展目标 3。"],
  "Can support SDG 3 when careful study monitoring helps protect participants and maintain the quality of health research.": ["Boleh menyokong SDG 3 apabila pemantauan kajian yang teliti membantu melindungi peserta dan mengekalkan kualiti penyelidikan kesihatan.", "当认真监查研究有助于保护参与者并维持健康研究的质量时，可支持可持续发展目标 3。"],
  "Can support SDG 12 through transparent reporting of organisational impacts and SDG 13 when climate impacts are measured and disclosed.": ["Boleh menyokong SDG 12 melalui pelaporan impak organisasi yang telus, serta SDG 13 apabila impak iklim diukur dan didedahkan.", "可通过透明报告组织影响支持可持续发展目标 12；当气候影响得到衡量和披露时，也可支持目标 13。"],
  "Can support SDG 12 when environmental metrics inform resource use and SDG 13 when they track climate-related impacts.": ["Boleh menyokong SDG 12 apabila metrik alam sekitar memaklumkan penggunaan sumber, serta SDG 13 apabila metrik itu menjejaki impak berkaitan iklim.", "当环境指标为资源使用提供依据时，可支持可持续发展目标 12；当其追踪气候相关影响时，也可支持目标 13。"],
  "Can support SDG 13 when accurate carbon accounting helps organisations measure and manage greenhouse-gas emissions.": ["Boleh menyokong SDG 13 apabila perakaunan karbon yang tepat membantu organisasi mengukur dan mengurus pelepasan gas rumah hijau.", "当准确的碳核算帮助组织衡量和管理温室气体排放时，可支持可持续发展目标 13。"],
  "Can support SDG 12 through responsible environmental compliance and SDG 13 when regulation addresses climate impacts.": ["Boleh menyokong SDG 12 melalui pematuhan alam sekitar yang bertanggungjawab, serta SDG 13 apabila peraturan menangani impak iklim.", "可通过负责任的环境合规支持可持续发展目标 12；当法规应对气候影响时，也可支持目标 13。"],
  "Can support SDG 12 when lifecycle assessment identifies resource and waste impacts, and SDG 13 when it evaluates emissions across a product lifecycle.": ["Boleh menyokong SDG 12 apabila penilaian kitar hayat mengenal pasti impak sumber dan sisa, serta SDG 13 apabila penilaian itu mengukur pelepasan sepanjang kitar hayat produk.", "当生命周期评估识别资源和废弃物影响时，可支持可持续发展目标 12；当其评估产品全生命周期的排放时，也可支持目标 13。"],
  "Can support SDG 7 when applied to reliable, affordable clean-energy systems and SDG 13 when those systems help reduce emissions.": ["Boleh menyokong SDG 7 apabila digunakan dalam sistem tenaga bersih yang boleh dipercayai dan mampu milik, serta SDG 13 apabila sistem itu membantu mengurangkan pelepasan.", "当应用于可靠且可负担的清洁能源系统时，可支持可持续发展目标 7；当这些系统帮助减少排放时，也可支持目标 13。"],
  "Can support SDG 7 when electrical engineering enables safe, efficient energy systems and SDG 9 when it strengthens infrastructure.": ["Boleh menyokong SDG 7 apabila kejuruteraan elektrik membolehkan sistem tenaga yang selamat dan cekap, serta SDG 9 apabila ia memperkukuh infrastruktur.", "当电气工程促成安全高效的能源系统时，可支持可持续发展目标 7；当其强化基础设施时，也可支持目标 9。"],
  "Can support SDG 9 when technical designs solve practical engineering needs and contribute to useful infrastructure or innovation.": ["Boleh menyokong SDG 9 apabila reka bentuk teknikal menyelesaikan keperluan kejuruteraan praktikal dan menyumbang kepada infrastruktur atau inovasi yang berguna.", "当技术设计解决实际工程需求并促进实用基础设施或创新时，可支持可持续发展目标 9。"],
  "Can support SDG 7 when simulations help evaluate clean-energy systems and SDG 13 when they inform lower-emission designs.": ["Boleh menyokong SDG 7 apabila simulasi membantu menilai sistem tenaga bersih, serta SDG 13 apabila simulasi memaklumkan reka bentuk yang menghasilkan pelepasan lebih rendah.", "当仿真帮助评估清洁能源系统时，可支持可持续发展目标 7；当其为低排放设计提供依据时，也可支持目标 13。"],
  "Can support SDG 7 when grid integration connects renewable energy reliably and SDG 9 when it strengthens energy infrastructure.": ["Boleh menyokong SDG 7 apabila integrasi grid menghubungkan tenaga boleh baharu dengan boleh dipercayai, serta SDG 9 apabila ia memperkukuh infrastruktur tenaga.", "当电网整合可靠地接入可再生能源时，可支持可持续发展目标 7；当其强化能源基础设施时，也可支持目标 9。"],
  "Can support SDG 9 when engineering safety practices help protect people and maintain dependable infrastructure and systems.": ["Boleh menyokong SDG 9 apabila amalan keselamatan kejuruteraan membantu melindungi orang ramai dan mengekalkan infrastruktur serta sistem yang boleh diharap.", "当工程安全实践帮助保护人员并维护可靠的基础设施和系统时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when well-designed control systems improve the reliable operation of industrial infrastructure.": ["Boleh menyokong SDG 9 apabila sistem kawalan yang direka dengan baik meningkatkan operasi infrastruktur industri yang boleh dipercayai.", "当设计良好的控制系统提升工业基础设施运行的可靠性时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when safe, reliable PLC programming supports useful industrial systems and infrastructure.": ["Boleh menyokong SDG 9 apabila pengaturcaraan PLC yang selamat dan boleh dipercayai menyokong sistem serta infrastruktur industri yang berguna.", "当安全可靠的 PLC 编程支持实用的工业系统和基础设施时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when responsibly designed automation improves industrial capability and system reliability.": ["Boleh menyokong SDG 9 apabila automasi yang direka secara bertanggungjawab meningkatkan keupayaan industri dan kebolehpercayaan sistem.", "当以负责任方式设计的自动化提升工业能力和系统可靠性时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when robotics is applied to useful, safe industrial innovation and infrastructure.": ["Boleh menyokong SDG 9 apabila robotik digunakan untuk inovasi dan infrastruktur industri yang berguna serta selamat.", "当机器人技术应用于实用、安全的工业创新和基础设施时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when equipment troubleshooting helps maintain reliable industrial systems and infrastructure.": ["Boleh menyokong SDG 9 apabila penyelesaian masalah peralatan membantu mengekalkan sistem dan infrastruktur industri yang boleh dipercayai.", "当设备故障排查帮助维护可靠的工业系统和基础设施时，可支持可持续发展目标 9。"],
  "Can support SDG 9 through reliable industrial processes and SDG 12 when quality systems help reduce defects, waste, and rework.": ["Boleh menyokong SDG 9 melalui proses industri yang boleh dipercayai, serta SDG 12 apabila sistem kualiti membantu mengurangkan kecacatan, sisa dan kerja semula.", "可通过可靠的工业流程支持可持续发展目标 9；当质量体系帮助减少缺陷、浪费和返工时，也可支持目标 12。"],
  "Can support SDG 9 by improving system reliability and SDG 12 when root-cause fixes prevent recurring defects and material waste.": ["Boleh menyokong SDG 9 dengan meningkatkan kebolehpercayaan sistem, serta SDG 12 apabila pembaikan punca utama mencegah kecacatan berulang dan pembaziran bahan.", "可通过提升系统可靠性支持可持续发展目标 9；当根因修复防止缺陷复发和材料浪费时，也可支持目标 12。"],
  "Can support SDG 9 when rigorous testing helps ensure that engineered products and systems work reliably.": ["Boleh menyokong SDG 9 apabila pengujian yang teliti membantu memastikan produk dan sistem kejuruteraan berfungsi dengan boleh dipercayai.", "当严格的测试帮助确保工程产品和系统可靠运行时，可支持可持续发展目标 9。"],
  "Can support SDG 9 through more reliable production and SDG 12 when process controls help reduce defects and wasted materials.": ["Boleh menyokong SDG 9 melalui pengeluaran yang lebih boleh dipercayai, serta SDG 12 apabila kawalan proses membantu mengurangkan kecacatan dan pembaziran bahan.", "可通过提升生产可靠性支持可持续发展目标 9；当流程控制帮助减少缺陷和材料浪费时，也可支持目标 12。"],
  "Can support SDG 9 when process improvements strengthen industrial capability and SDG 12 when they use resources more efficiently.": ["Boleh menyokong SDG 9 apabila penambahbaikan proses memperkukuh keupayaan industri, serta SDG 12 apabila sumber digunakan dengan lebih cekap.", "当流程改进强化工业能力时，可支持可持续发展目标 9；当其提升资源使用效率时，也可支持目标 12。"],
  "Can support SDG 9 when carefully validated inspection automation improves industrial systems and SDG 12 when it prevents defects and waste.": ["Boleh menyokong SDG 9 apabila automasi pemeriksaan yang disahkan dengan teliti menambah baik sistem industri, serta SDG 12 apabila ia mencegah kecacatan dan sisa.", "当经过仔细验证的检测自动化改进工业系统时，可支持可持续发展目标 9；当其防止缺陷和浪费时，也可支持目标 12。"],
  "Can support SDG 4 when learning design creates inclusive, relevant opportunities for people to build knowledge and skills.": ["Boleh menyokong SDG 4 apabila reka bentuk pembelajaran menyediakan peluang inklusif dan relevan untuk membina pengetahuan serta kemahiran.", "当学习设计创造包容且切合需求的机会，帮助人们培养知识和技能时，可支持可持续发展目标 4。"],
  "Can support SDG 4 when fair, well-aligned assessments help learners demonstrate and develop their knowledge.": ["Boleh menyokong SDG 4 apabila penilaian yang adil dan selaras membantu pelajar menunjukkan serta mengembangkan pengetahuan mereka.", "当公平且设计合理的评估帮助学习者展示并发展知识时，可支持可持续发展目标 4。"],
  "Can support SDG 4 when accurate, accessible learning content helps people participate in quality education.": ["Boleh menyokong SDG 4 apabila kandungan pembelajaran yang tepat dan mudah diakses membantu orang menyertai pendidikan berkualiti.", "当准确且易于获取的学习内容帮助人们参与优质教育时，可支持可持续发展目标 4。"],
  "Can support SDG 4 when learning technologies are accessible and effectively support teaching and learning.": ["Boleh menyokong SDG 4 apabila teknologi pembelajaran mudah diakses dan menyokong pengajaran serta pembelajaran dengan berkesan.", "当学习技术易于使用并有效支持教与学时，可支持可持续发展目标 4。"],
  "Can support SDG 4 by making learning accessible and SDG 10 when inclusive design reduces barriers for people with different needs.": ["Boleh menyokong SDG 4 dengan menjadikan pembelajaran mudah diakses, serta SDG 10 apabila reka bentuk inklusif mengurangkan halangan bagi mereka yang mempunyai keperluan berbeza.", "可通过提升学习的可及性支持可持续发展目标 4；当包容性设计减少不同需求人群面临的障碍时，也可支持目标 10。"],
  "Can support SDG 4 when responsible learning analytics help educators identify barriers and improve learning experiences.": ["Boleh menyokong SDG 4 apabila analitik pembelajaran yang bertanggungjawab membantu pendidik mengenal pasti halangan dan menambah baik pengalaman pembelajaran.", "当负责任的学习分析帮助教育者识别障碍并改善学习体验时，可支持可持续发展目标 4。"],
  "Can support SDG 9 when user research informs better digital products and SDG 10 when research includes people whose needs are often overlooked.": ["Boleh menyokong SDG 9 apabila penyelidikan pengguna memaklumkan produk digital yang lebih baik, serta SDG 10 apabila penyelidikan merangkumi mereka yang keperluannya sering terpinggir.", "当用户研究为更好的数字产品提供依据时，可支持可持续发展目标 9；当研究纳入需求常被忽视的人群时，也可支持目标 10。"],
  "Can support SDG 9 through useful digital-product innovation and SDG 10 when interaction design makes products more inclusive.": ["Boleh menyokong SDG 9 melalui inovasi produk digital yang berguna, serta SDG 10 apabila reka bentuk interaksi menjadikan produk lebih inklusif.", "可通过实用的数字产品创新支持可持续发展目标 9；当交互设计让产品更具包容性时，也可支持目标 10。"],
  "Can support SDG 9 when prototypes help teams test and improve practical products, services, or infrastructure.": ["Boleh menyokong SDG 9 apabila prototaip membantu pasukan menguji dan menambah baik produk, perkhidmatan atau infrastruktur yang praktikal.", "当原型帮助团队测试和改进实用产品、服务或基础设施时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when usability testing improves digital products and SDG 10 when testing includes users with diverse needs.": ["Boleh menyokong SDG 9 apabila pengujian kebolehgunaan menambah baik produk digital, serta SDG 10 apabila pengujian melibatkan pengguna dengan pelbagai keperluan.", "当可用性测试改进数字产品时，可支持可持续发展目标 9；当测试纳入需求多样的用户时，也可支持目标 10。"],
  "Can support SDG 9 when clear information architecture makes digital services and information easier to navigate.": ["Boleh menyokong SDG 9 apabila seni bina maklumat yang jelas memudahkan navigasi perkhidmatan digital dan maklumat.", "当清晰的信息架构让数字服务和信息更易于浏览时，可支持可持续发展目标 9。"],
  "Can support SDG 9 through useful product communication and SDG 10 when visual design is accessible and represents diverse users.": ["Boleh menyokong SDG 9 melalui komunikasi produk yang berguna, serta SDG 10 apabila reka bentuk visual mudah diakses dan mewakili pengguna yang pelbagai.", "可通过实用的产品沟通支持可持续发展目标 9；当视觉设计易于使用并体现多元用户时，也可支持目标 10。"],
  "Can support SDG 4 through responsible AI learning and SDG 8 when AI literacy helps people adapt to changes in work.": ["Boleh menyokong SDG 4 melalui pembelajaran AI yang bertanggungjawab, serta SDG 8 apabila literasi AI membantu orang menyesuaikan diri dengan perubahan pekerjaan.", "可通过负责任的 AI 学习支持可持续发展目标 4；当 AI 素养帮助人们适应工作变化时，也可支持目标 8。"],
  "Can support SDG 8 through organised, responsible work and SDG 9 when projects deliver useful infrastructure or innovation.": ["Boleh menyokong SDG 8 melalui kerja yang teratur dan bertanggungjawab, serta SDG 9 apabila projek menghasilkan infrastruktur atau inovasi yang berguna.", "可通过有组织且负责任的工作支持可持续发展目标 8；当项目交付实用基础设施或创新时，也可支持目标 9。"],
  "Can support SDG 8 when responsible leadership promotes safe, fair, and productive work.": ["Boleh menyokong SDG 8 apabila kepimpinan yang bertanggungjawab menggalakkan kerja yang selamat, adil dan produktif.", "当负责任的领导力促进安全、公平且高效的工作时，可支持可持续发展目标 8。"],
  "Can support SDG 8 when respectful teamwork supports collaboration and decent working conditions.": ["Boleh menyokong SDG 8 apabila kerja berpasukan yang saling menghormati menyokong kerjasama dan keadaan kerja yang wajar.", "当相互尊重的团队合作促进协作和体面工作条件时，可支持可持续发展目标 8。"],
  "Can support SDG 8 through well-managed event work and SDG 12 when planning reduces unnecessary materials and waste.": ["Boleh menyokong SDG 8 melalui pengurusan acara yang baik, serta SDG 12 apabila perancangan mengurangkan penggunaan bahan dan sisa yang tidak perlu.", "可通过妥善管理活动工作支持可持续发展目标 8；当规划减少不必要的材料使用和浪费时，也可支持目标 12。"],
  "Can support SDG 8 when practical problem-solving improves work and SDG 9 when it helps develop or improve useful systems.": ["Boleh menyokong SDG 8 apabila penyelesaian masalah praktikal menambah baik kerja, serta SDG 9 apabila ia membantu membangunkan atau menambah baik sistem yang berguna.", "当实际的问题解决能力改善工作时，可支持可持续发展目标 8；当其帮助开发或改进实用系统时，也可支持目标 9。"],
  "Can support SDG 9 when reliable semiconductor processes help manufacture the chips that power industry, research, and public services.": ["Boleh menyokong SDG 9 apabila proses semikonduktor yang boleh dipercayai membantu menghasilkan cip yang menjana industri, penyelidikan dan perkhidmatan awam.", "当可靠的半导体工艺助力制造驱动工业、研究和公共服务的芯片时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when dependable IT and data-center operations keep critical digital services running for industry and the public.": ["Boleh menyokong SDG 9 apabila operasi IT dan pusat data yang boleh diharap memastikan perkhidmatan digital kritikal terus berjalan untuk industri dan orang awam.", "当可靠的 IT 与数据中心运营让工业和公众所需的关键数字服务持续运行时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when automated delivery pipelines make software and platform services more reliable and responsive.": ["Boleh menyokong SDG 9 apabila saluran penghantaran automatik menjadikan perisian dan perkhidmatan platform lebih boleh dipercayai dan responsif.", "当自动化交付流水线让软件与平台服务更可靠、响应更及时时，可支持可持续发展目标 9。"],
  "Can support SDG 9 when proactive monitoring keeps networks and systems reliable and prevents service disruption.": ["Boleh menyokong SDG 9 apabila pemantauan proaktif memastikan rangkaian dan sistem kekal boleh dipercayai serta mengelakkan gangguan perkhidmatan.", "当主动监测保持网络与系统可靠并防止服务中断时，可支持可持续发展目标 9。"],
  "Can support SDG 9 through responsible, transparent AI innovation and SDG 16 when systems are governed fairly and accountably.": ["Boleh menyokong SDG 9 melalui inovasi AI yang bertanggungjawab dan telus, serta SDG 16 apabila sistem ditadbir secara adil dan akauntabel.", "可通过负责任、透明的 AI 创新支持可持续发展目标 9；当系统得到公平且负责的治理时，也可支持目标 16。"],
  "Can support SDG 7 when efficient electro-mechanical systems reduce energy use in mobility and industry, and SDG 9 when they advance manufacturing automation.": ["Boleh menyokong SDG 7 apabila sistem elektro-mekanikal yang cekap mengurangkan penggunaan tenaga dalam mobiliti dan industri, serta SDG 9 apabila ia memajukan automasi pembuatan.", "当高效的机电系统降低出行与工业的能耗时，可支持可持续发展目标 7；当它们推动制造自动化时，也可支持目标 9。"],
  "Can support SDG 7 when efficient production processes reduce energy use, and SDG 9 when they make manufacturing and industrial systems more reliable.": ["Boleh menyokong SDG 7 apabila proses pengeluaran yang cekap mengurangkan penggunaan tenaga, serta SDG 9 apabila ia menjadikan sistem pembuatan dan perindustrian lebih boleh dipercayai.", "当高效的生产流程降低能耗时，可支持可持续发展目标 7；当它们让制造与工业系统更可靠时，也可支持目标 9。"],
  "Can support SDG 9 when auditing algorithms makes AI systems more trustworthy, and SDG 16 when it helps keep automated decisions fair and accountable.": ["Boleh menyokong SDG 9 apabila pengauditan algoritma menjadikan sistem AI lebih dipercayai, serta SDG 16 apabila ia membantu memastikan keputusan automatik adil dan akauntabel.", "当算法审计让 AI 系统更值得信赖时，可支持可持续发展目标 9；当它帮助保持自动化决策公平可问责时，也可支持目标 16。"],
  "Can support SDG 8 through fair, compliant business practice and SDG 16 when transparent reporting strengthens accountable institutions.": ["Boleh menyokong SDG 8 melalui amalan perniagaan yang adil dan patuh, serta SDG 16 apabila pelaporan telus mengukuhkan institusi yang akauntabel.", "可通过公平合规的商业实践支持可持续发展目标 8；当透明报告强化问责机构时，也可支持目标 16。"],
  "Can support SDG 3 when quality manufacturing protects patient safety, and SDG 9 through reliable production and quality infrastructure.": ["Boleh menyokong SDG 3 apabila pembuatan berkualiti melindungi keselamatan pesakit, serta SDG 9 melalui pengeluaran dan infrastruktur kualiti yang boleh dipercayai.", "当高质量制造保障患者安全时，可支持可持续发展目标 3；通过可靠的生产与质量基础设施，也可支持目标 9。"],
  "Can support SDG 7 when grid-scale storage makes renewable energy more usable, and SDG 9 through a more resilient electricity grid.": ["Boleh menyokong SDG 7 apabila storan berskala grid menjadikan tenaga boleh diperbaharui lebih mudah digunakan, serta SDG 9 melalui grid elektrik yang lebih berdaya tahan.", "当电网级储能让可再生能源更易利用时，可支持可持续发展目标 7；通过更具韧性的电网，也可支持目标 9。"],
  "Can support SDG 8 through productive digital-content work and SDG 9 when pipeline tooling improves how creative software is produced.": ["Boleh menyokong SDG 8 melalui kerja kandungan digital yang produktif, serta SDG 9 apabila perkakas saluran kerja menambah baik cara perisian kreatif dihasilkan.", "可通过高效的数字内容创作支持可持续发展目标 8；当流程工具改善创意软件的产出方式时，也可支持目标 9。"],
  "Can support SDG 8 through efficient, well-managed supply chains and SDG 9 when better logistics planning improves industry infrastructure.": ["Boleh menyokong SDG 8 melalui rantaian bekalan yang cekap dan terurus, serta SDG 9 apabila perancangan logistik yang lebih baik menambah baik infrastruktur industri.", "可通过高效、管理良好的供应链支持可持续发展目标 8；当更完善的物流规划改善工业基础设施时，也可支持目标 9。"],
  "Can support SDG 8 when well-planned operations make work more efficient, and SDG 9 when optimisation improves the systems that deliver products and services.": ["Boleh menyokong SDG 8 apabila operasi yang dirancang dengan baik menjadikan kerja lebih cekap, serta SDG 9 apabila pengoptimuman menambah baik sistem yang menyampaikan produk dan perkhidmatan.", "当规划完善的运营让工作更高效时，可支持可持续发展目标 8；当优化改善交付产品与服务的系统时，也可支持目标 9。"],
  "Can support SDG 9 through durable engineering design and SDG 11 when safe structural work helps build resilient communities and infrastructure.": ["Boleh menyokong SDG 9 melalui reka bentuk kejuruteraan yang tahan lama, serta SDG 11 apabila kerja struktur yang selamat membantu membina komuniti dan infrastruktur yang berdaya tahan.", "可通过耐久的工程设计支持可持续发展目标 9；当安全的结构工程帮助打造韧性社区与基础设施时，也可支持目标 11。"],
  "Can support SDG 9 through sound foundation engineering and SDG 11 when managing ground risk protects people and infrastructure.": ["Boleh menyokong SDG 9 melalui kejuruteraan asas yang kukuh, serta SDG 11 apabila pengurusan risiko tanah melindungi orang dan infrastruktur.", "可通过扎实的基础工程支持可持续发展目标 9；当地质风险管理保护民众与基础设施时，也可支持目标 11。"],
  "Can support SDG 8 through fair, certified trade and SDG 12 when auditing standards support responsible production and consumption.": ["Boleh menyokong SDG 8 melalui perdagangan yang adil dan diperakui, serta SDG 12 apabila piawaian pengauditan menyokong pengeluaran dan penggunaan yang bertanggungjawab.", "可通过公平、认证的贸易支持可持续发展目标 8；当审计标准支持负责任的产销时，也可支持目标 12。"],
};

const fpLocaleIndex = locale => FP_LOCALES.indexOf(locale);
const fpIntlLocale = locale => locale === "zh" ? "zh-CN" : locale === "ms" ? "ms-MY" : "en-GB";
const fpTranslation = (text, locale) => {
  const index = fpLocaleIndex(locale);
  if (index <= 0) return text;
  const skillJustification = FP_SKILL_SDG_TEXT[text];
  if (skillJustification && index > 0) return skillJustification[index - 1];
  const values = FP_TEXT[text];
  if (values && index >= 0) return values[index];
  if (index < 0) return text;
  const step = text.match(/^STEP (\d+) OF 4$/);
  if (step) return locale === "zh" ? `第 ${step[1]} 步，共 4 步` : `LANGKAH ${step[1]} DARIPADA 4`;
  const savedPeople = text.match(/^SAVED PEOPLE \((\d+)\)$/);
  if (savedPeople) return locale === "zh" ? `已保存的档案（${savedPeople[1]}）` : `PROFIL TERSIMPAN (${savedPeople[1]})`;
  const deletePrompt = text.match(/^Delete (.+)\? This can't be undone\.$/);
  if (deletePrompt) return locale === "zh"
    ? `删除${deletePrompt[1]}？此操作无法撤销。`
    : `Padam ${deletePrompt[1]}? Tindakan ini tidak boleh dibuat asal.`;
  const lastUpdated = text.match(/^Signals last updated: (.+) ·$/);
  if (lastUpdated) return locale === "zh"
    ? `趋势信号最近更新：${lastUpdated[1]} ·`
    : `Isyarat terakhir dikemas kini: ${lastUpdated[1]} ·`;
  const signalCount = text.match(/^(\d+) signals$/);
  if (signalCount) return locale === "zh" ? `${signalCount[1]} 条信号` : `${signalCount[1]} isyarat`;
  const linkedGoals = text.match(/^(\d+) of the (\d+) goals are linked to our roles \(highlighted\)\.$/);
  if (linkedGoals) return locale === "zh"
    ? `我们的职业关联了 ${linkedGoals[1]} 项可持续发展目标（已突出显示），共 ${linkedGoals[2]} 项。`
    : `${linkedGoals[1]} daripada ${linkedGoals[2]} matlamat dikaitkan dengan kerjaya kami (ditandakan).`;
  const weekCount = text.match(/^\+(\d+)$/);
  if (weekCount) return `+${weekCount[1]}`;
  const seeMore = text.match(/^See more \((\d+)\)$/);
  if (seeMore) return locale === "zh" ? `查看更多（${seeMore[1]}）` : `Lihat lagi (${seeMore[1]})`;
  const qwenCounts = text.match(/^Qwen on RunPod suggested (\d+) skills; the local dictionary added (\d+) more\. Review all evidence and proficiency levels\.$/);
  if (qwenCounts) return locale === "zh"
    ? `RunPod 上的 Qwen 建议了 ${qwenCounts[1]} 项技能；本地词典另外补充了 ${qwenCounts[2]} 项。请核对所有证据和熟练程度。`
    : `Qwen di RunPod mencadangkan ${qwenCounts[1]} kemahiran; kamus tempatan menambah ${qwenCounts[2]} lagi. Semak semua bukti dan tahap kemahiran.`;
  const qwenNone = text.match(/^Qwen completed analysis but returned no validated skill suggestions\. The local dictionary found (\d+) possible skills; review them carefully\.$/);
  if (qwenNone) return locale === "zh"
    ? `Qwen 已完成分析，但没有返回经验证的技能建议。本地词典找到 ${qwenNone[1]} 项可能的技能，请仔细核对。`
    : `Qwen telah selesai menganalisis tetapi tiada cadangan kemahiran yang disahkan. Kamus tempatan menemui ${qwenNone[1]} kemahiran yang mungkin; semak dengan teliti.`;
  // CV detail hints on the Check step: "<label>: <value from the CV>"; the value stays as written in the CV.
  const hintLabel = text.match(/^(Current role|Education \(may be in progress\)|Highest completed qualification \(confirm\)|Industry|Project|Achievement|Certification): (.+)$/);
  if (hintLabel) {
    const labels = { "Industry": ["Industri", "行业"], "Project": ["Projek", "项目"], "Achievement": ["Pencapaian", "成就"], "Certification": ["Pensijilan", "证书"] };
    const label = labels[hintLabel[1]] ? labels[hintLabel[1]][locale === "zh" ? 1 : 0] : fpTranslation(hintLabel[1], locale);
    return `${label}${locale === "zh" ? "：" : ": "}${hintLabel[2]}`;
  }
  const hintEvidence = text.match(/^CV evidence: (“.+”)$/);
  if (hintEvidence) return `${locale === "zh" ? "简历证据：" : "Bukti CV: "}${hintEvidence[1]}`;
  const cvQuote = text.match(/^CV evidence \((Qwen AI|Claude AI|local dictionary)\): (“.+”)(?: \(page (\d+)\))?$/);
  if (cvQuote) {
    const by = cvQuote[1] === "local dictionary" ? (locale === "zh" ? "本地词典" : "kamus tempatan") : cvQuote[1];
    return locale === "zh"
      ? `简历证据（${by}）：${cvQuote[2]}${cvQuote[3] ? `（第 ${cvQuote[3]} 页）` : ""}`
      : `Bukti CV (${by}): ${cvQuote[2]}${cvQuote[3] ? ` (halaman ${cvQuote[3]})` : ""}`;
  }
  const readBy = text.match(/^Read by: (.+?)( \(Anthropic\)| on RunPod)?$/);
  if (readBy) return (locale === "zh" ? "读取方式：" : "Dibaca oleh: ") + fpTranslation(readBy[1], locale)
    + (readBy[2] === " on RunPod" ? (locale === "zh" ? "（RunPod）" : " di RunPod") : readBy[2] ? " (Anthropic)" : "");
  const belowLevel = text.match(/^◐ (.+) (\d+)\/(\d+)$/);
  if (belowLevel) return `◐ ${fpTranslation(belowLevel[1], locale)} ${belowLevel[2]}/${belowLevel[3]}`;
  const levelTip = text.match(/^Your level (\d+), this career needs (\d+)$/);
  if (levelTip) return locale === "zh" ? `你的水平为 ${levelTip[1]}，此职业需要 ${levelTip[2]}` : `Tahap anda ${levelTip[1]}, kerjaya ini memerlukan ${levelTip[2]}`;
  const skillChange = text.match(/^([✓+]) (.+)$/);
  if (skillChange) return `${skillChange[1]} ${fpTranslation(skillChange[2], locale)}`;
  const moveCount = text.match(/^\((\d+)\)$/);
  if (moveCount) return locale === "zh" ? `（${moveCount[1]}）` : `(${moveCount[1]})`;
  const priority = text.match(/^Priority (\d+)$/);
  if (priority) return `${fpTranslation("Priority", locale)} ${priority[1]}`;
  const studyDuration = text.match(/^(\d+(?:\.\d+)?) (hours?|weeks?|h)( \(estimated\))?$/);
  if (studyDuration) return locale === "zh"
    ? `${studyDuration[1]}${studyDuration[2].startsWith("week") ? " 周" : " 小时"}${studyDuration[3] ? "（估算）" : ""}`
    : `${studyDuration[1]} ${studyDuration[2].startsWith("week") ? "minggu" : "jam"}${studyDuration[3] ? " (anggaran)" : ""}`;
  const pathIntro = text.match(/^(Fast|Moderate) AI disruption · (\d+) h a week · free, low-cost and HRD Corp claimable courses$/);
  if (pathIntro) return locale === "zh"
    ? `${pathIntro[1] === "Fast" ? "快速" : "温和"}的 AI 冲击 · 每周 ${pathIntro[2]} 小时 · 免费、低价及可申请 HRD Corp 资助的课程`
    : `Gangguan AI ${pathIntro[1] === "Fast" ? "pantas" : "sederhana"} · ${pathIntro[2]} jam seminggu · kursus percuma, kos rendah dan boleh dituntut melalui HRD Corp`;
  const fastDemand = text.match(/^Fast AI: demand (\d+) → (\d+)$/);
  if (fastDemand) return locale === "zh" ? `快速 AI：需求 ${fastDemand[1]} → ${fastDemand[2]}` : `AI pantas: permintaan ${fastDemand[1]} → ${fastDemand[2]}`;
  const aiShare = text.match(/^(\d+) of (\d+) signals are about AI and count double$/);
  if (aiShare) return locale === "zh"
    ? `${aiShare[2]} 条信号中有 ${aiShare[1]} 条与 AI 相关，按双倍计算`
    : `${aiShare[1]} daripada ${aiShare[2]} isyarat berkaitan AI dan dikira dua kali`;
  const scenarioImpact = text.match(/^Right now this changes demand for (\d+) of (\d+) careers \(([+−]?\d+) to ([+−]?\d+) points\) and (\d+) careers change rank\.$/);
  if (scenarioImpact) return locale === "zh"
    ? `目前，这会改变 ${scenarioImpact[2]} 个职业中 ${scenarioImpact[1]} 个的需求（${scenarioImpact[3]} 至 ${scenarioImpact[4]} 分），并有 ${scenarioImpact[5]} 个职业排名发生变化。`
    : `Kini, ini mengubah permintaan bagi ${scenarioImpact[1]} daripada ${scenarioImpact[2]} kerjaya (${scenarioImpact[3]} hingga ${scenarioImpact[4]} mata) dan ${scenarioImpact[5]} kerjaya berubah kedudukan.`;
  const noAiCareers = text.match(/^(\d+) careers? (?:has|have) no AI-related signals yet, so (?:its|their) demand stays the same\.$/);
  if (noAiCareers) return locale === "zh"
    ? `有 ${noAiCareers[1]} 个职业尚无与 AI 相关的信号，因此需求保持不变。`
    : `${noAiCareers[1]} kerjaya belum mempunyai isyarat berkaitan AI, jadi permintaannya kekal sama.`;
  const pctDemand = text.match(/^Demand ±(\d+)$/);
  if (pctDemand) return locale === "zh" ? `需求 ±${pctDemand[1]}` : `Permintaan ±${pctDemand[1]}`;
  const demandScore = text.match(/^Demand (\d+)$/);
  if (demandScore) return locale === "zh" ? `需求 ${demandScore[1]}` : `Permintaan ${demandScore[1]}`;
  const skillScore = text.match(/^Skills (\d+)$/);
  if (skillScore) return locale === "zh" ? `技能 ${skillScore[1]}` : `Kemahiran ${skillScore[1]}`;
  const resultSkills = text.match(/^Skills (\d+) · Demand (\d+)$/);
  if (resultSkills) return locale === "zh"
    ? `技能 ${resultSkills[1]} · 需求 ${resultSkills[2]}`
    : `Kemahiran ${resultSkills[1]} · Permintaan ${resultSkills[2]}`;
  const signalConfidence = text.match(/^(\d+) dated signals? behind demand \((.+) confidence\)\.$/);
  if (signalConfidence) return locale === "zh"
    ? `需求依据 ${signalConfidence[1]} 条带日期的趋势信号（${signalConfidence[2]} 置信度）。`
    : `${signalConfidence[1]} isyarat bertarikh menjadi asas permintaan (keyakinan ${signalConfidence[2]}).`;
  const sharedInterests = text.match(/^You share (.+) interests with this career\.$/);
  if (sharedInterests) {
    const interests = sharedInterests[1].split(", ").map(x => fpTranslation(x, locale)).join(locale === "zh" ? "、" : ", ");
    return locale === "zh" ? `你的兴趣类型与此职业相符：${interests}。` : `Anda berkongsi minat ${interests} dengan kerjaya ini.`;
  }
  const prefixedPlus = text.match(/^\+ (.+)$/);
  if (prefixedPlus) return `+ ${fpTranslation(prefixedPlus[1], locale)}`;
  const feedLastChecked = text.match(/^Live feeds last checked (.+?)( · refreshes automatically (.+)| · refreshed manually)?$/);
  if (feedLastChecked) return locale === "zh"
    ? `实时信息源上次检查时间：${feedLastChecked[1]}${feedLastChecked[3] ? ` · 自动刷新${feedLastChecked[3]}` : feedLastChecked[0].endsWith("refreshed manually") ? " · 手动刷新" : ""}`
    : `Suapan langsung terakhir disemak ${feedLastChecked[1]}${feedLastChecked[3] ? ` · dimuat semula secara automatik ${feedLastChecked[3]}` : feedLastChecked[0].endsWith("refreshed manually") ? " · dimuat semula secara manual" : ""}`;
  const noFeedStatus = text.match(/^Live feeds not checked yet; showing dated reports only( · refreshed manually)?$/);
  if (noFeedStatus) return locale === "zh"
    ? `实时信息源尚未检查；目前仅显示带日期的报告${noFeedStatus[1] ? " · 手动刷新" : ""}`
    : `Suapan langsung belum disemak; laporan bertarikh sahaja dipaparkan${noFeedStatus[1] ? " · dimuat semula secara manual" : ""}`;
  const lastRun = text.match(/^● (OK|Running|Failed) · (\d+) accepted · (.+)$/);
  if (lastRun) return locale === "zh"
    ? `● ${lastRun[1] === "OK" ? "正常" : lastRun[1] === "Running" ? "运行中" : "失败"} · 已接收 ${lastRun[2]} 条 · ${lastRun[3]}`
    : `● ${lastRun[1] === "OK" ? "OK" : lastRun[1] === "Running" ? "Sedang berjalan" : "Gagal"} · ${lastRun[2]} diterima · ${lastRun[3]}`;
  const feedItems = text.match(/^(.+): (\d+) items$/);
  if (feedItems) return `${feedItems[1]}: ${feedItems[2]} ${locale === "zh" ? "条" : "item"}`;
  const refreshInterval = text.match(/^every (\d+) h$/);
  if (refreshInterval) return locale === "zh" ? `每 ${refreshInterval[1]} 小时` : `setiap ${refreshInterval[1]} jam`;
  const refreshSummary = text.match(/^Refresh (.+): checked (\d+) items, (\d+) new signals, (\d+) rejected, (\d+) failed \(tagged by (.+)\)\.$/);
  if (refreshSummary) return locale === "zh"
    ? `刷新${refreshSummary[1]}：检查了 ${refreshSummary[2]} 条，新增信号 ${refreshSummary[3]} 条，拒绝 ${refreshSummary[4]} 条，失败 ${refreshSummary[5]} 条（标注方式：${refreshSummary[6]}）。`
    : `Muat semula ${refreshSummary[1]}: ${refreshSummary[2]} item disemak, ${refreshSummary[3]} isyarat baharu, ${refreshSummary[4]} ditolak, ${refreshSummary[5]} gagal (ditandai oleh ${refreshSummary[6]}).`;
  const feedCheck = text.match(/^Claude: (configured|not configured) · RunPod: (configured|not configured) \(configuration is not a live health test\)$/);
  if (feedCheck) return locale === "zh"
    ? `Claude：${fpTranslation(feedCheck[1], locale)} · RunPod：${fpTranslation(feedCheck[2], locale)}（配置状态不代表实时健康检查）`
    : `Claude: ${fpTranslation(feedCheck[1], locale)} · RunPod: ${fpTranslation(feedCheck[2], locale)}（konfigurasi bukan ujian kesihatan langsung）`;
  const providerResult = text.match(/^Provider: (.+) · (\d+) grounded suggestions( · fallback: (.+))?$/);
  if (providerResult) return locale === "zh"
    ? `服务商：${providerResult[1]} · ${providerResult[2]} 条有依据的建议${providerResult[4] ? ` · 备用方案：${providerResult[4]}` : ""}`
    : `Penyedia: ${providerResult[1]} · ${providerResult[2]} cadangan berasaskan bukti${providerResult[4] ? ` · sandaran: ${providerResult[4]}` : ""}`;
  const savedSkills = text.match(/^Saved (\d+) confirmed skill entries in demo profile\. Suggested but unchecked skills were not saved\.$/);
  if (savedSkills) return locale === "zh"
    ? `已将 ${savedSkills[1]} 项已确认技能保存到演示档案。未勾选的建议技能不会保存。`
    : `${savedSkills[1]} kemahiran yang disahkan telah disimpan ke profil demo. Kemahiran cadangan yang tidak ditandakan tidak disimpan.`;
  const evidence = text.match(/^Evidence: “(.+)”$/);
  if (evidence) return `${fpTranslation("Evidence:", locale)} “${evidence[1]}”`;
  const savedAt = text.match(/^saved (.+)$/);
  if (savedAt) return `${fpTranslation("saved", locale)} ${savedAt[1]}`;
  const skillTotal = text.match(/^(\d+) skills$/);
  if (skillTotal) return locale === "zh" ? `${skillTotal[1]} 项技能` : `${skillTotal[1]} kemahiran`;
  const errorPrefix = text.match(/^(Refresh failed: |Save error: |Error: |Could not delete: )(.+)$/);
  if (errorPrefix) return `${fpTranslation(errorPrefix[1].trim(), locale)} ${errorPrefix[2]}`;
  const leadingSeparator = text.match(/^·\s+/);
  if (leadingSeparator) return `${leadingSeparator[0]}${fpTranslation(text.slice(leadingSeparator[0].length), locale)}`;
  if (text.includes(" · ")) return text.split(" · ").map(part => fpTranslation(part, locale)).join(" · ");
  const interestSummary = text.match(/^Interest fit counts for 20%\. Your strongest interests: (.+)\.$/);
  if (interestSummary) return `${fpTranslation("Interest fit counts for 20%. Your strongest interests:", locale)} ${interestSummary[1]}.`;
  const changeSummary = text.match(/^(\d+) new signals from the refresh on (.+)\.$/);
  if (changeSummary) return locale === "zh"
    ? `于 ${changeSummary[2]} 刷新后新增 ${changeSummary[1]} 条趋势信号。`
    : `${changeSummary[1]} isyarat trend baharu selepas kemas kini pada ${changeSummary[2]}.`;
  const roleMove = text.match(/^(.+) moved (up|down) from #(\d+) to #(\d+)$/);
  if (roleMove) {
    const title = fpTranslation(roleMove[1], locale);
    return locale === "zh"
      ? `${title}排名${roleMove[2] === "up" ? "上升" : "下降"}：从第 ${roleMove[3]} 名变为第 ${roleMove[4]} 名`
      : `${title} bergerak ${roleMove[2] === "up" ? "naik" : "turun"} daripada #${roleMove[3]} kepada #${roleMove[4]}`;
  }
  const roleStayed = text.match(/^(.+) stayed at #(\d+)$/);
  if (roleStayed) return locale === "zh"
    ? `${fpTranslation(roleStayed[1], locale)}仍排在第 ${roleStayed[2]} 名`
    : `${fpTranslation(roleStayed[1], locale)} kekal pada kedudukan #${roleStayed[2]}`;
  const trendMove = text.match(/^Trends (.+) → (.+) from (\d+) new signals?$/);
  if (trendMove) return locale === "zh"
    ? `趋势由 ${trendMove[1]} 变为 ${trendMove[2]}，新增 ${trendMove[3]} 条信号`
    : `Trend berubah daripada ${trendMove[1]} kepada ${trendMove[2]} daripada ${trendMove[3]} isyarat baharu`;
  const trCount = text.match(/^(Rising skills|Declining skills & jobs) \((\d+)\)$/);
  if (trCount) return `${fpTranslation(trCount[1], locale)} (${trCount[2]})`;
  const trBadge = text.match(/^([↑↓]) (\d+) (signals?|reports?)$/);
  if (trBadge) return locale === "zh" ? `${trBadge[1]} ${trBadge[2]} ${trBadge[3].startsWith("signal") ? "条信号" : "份报告"}` : `${trBadge[1]} ${trBadge[2]} ${trBadge[3].startsWith("signal") ? "isyarat" : "laporan"}`;
  const trLead = text.match(/^(Latest|Source): (.+)$/);
  if (trLead) return `${locale === "zh" ? (trLead[1] === "Latest" ? "最新：" : "来源：") : (trLead[1] === "Latest" ? "Terkini: " : "Sumber: ")}${trLead[2]}`;
  const pathProg = text.match(/^steps completed · (\d+) of (\d+) hours done$/);
  if (pathProg) return locale === "zh" ? `已完成步骤 · 已完成 ${pathProg[1]} / ${pathProg[2]} 小时` : `langkah selesai · ${pathProg[1]} daripada ${pathProg[2]} jam selesai`;
  const verificationDate = text.match(/^(Provider page checked|Source catalogue snapshot) (.+)$/);
  if (verificationDate) {
    const label = verificationDate[1] === "Provider page checked"
      ? fpTranslation("Provider page checked", locale)
      : fpTranslation("Source catalogue snapshot", locale);
    return `${label} ${verificationDate[2]}`;
  }
  const leadingStatus = text.match(/^(No checked course yet|No dated signal|Review skill requirements|General context|Linked through skills only)(.*)$/);
  if (leadingStatus && leadingStatus[2]) return `${fpTranslation(leadingStatus[1], locale)}${leadingStatus[2]}`;
  if (text.includes(", ")) {
    const names = text.split(", ");
    if (names.every(name => FP_TEXT[name])) return names.map(name => fpTranslation(name, locale)).join(locale === "zh" ? "、" : ", ");
  }
  const skillSdgSuffix = text.match(/^(.+) These are potential links, not guaranteed outcomes\.$/);
  if (skillSdgSuffix) return `${fpTranslation(skillSdgSuffix[1], locale)} ${fpTranslation("These are potential links, not guaranteed outcomes.", locale)}`;
  const goal = text.match(/^SDG (\d+) · (.+)$/);
  if (goal) {
    const name = fpTranslation(goal[2], locale);
    return locale === "zh" ? `可持续发展目标 ${goal[1]} · ${name}` : `SDG ${goal[1]} · ${name}`;
  }
  const sdgDescription = text.match(/^SDG (\d+): (.+?)( · (linked|not linked yet))?$/);
  if (sdgDescription) {
    const name = fpTranslation(sdgDescription[2], locale);
    const linked = sdgDescription[4] ? ` · ${fpTranslation(sdgDescription[4], locale)}` : "";
    return locale === "zh" ? `可持续发展目标 ${sdgDescription[1]}：${name}${linked}` : `SDG ${sdgDescription[1]}: ${name}${linked}`;
  }
  const action = text.match(/^(Build|Assess): (.+)$/);
  if (action) {
    const verb = action[1] === "Build"
      ? (locale === "zh" ? "提升" : "Bina")
      : (locale === "zh" ? "评估" : "Nilai");
    return `${verb}: ${fpTranslation(action[2], locale)}`;
  }
  const fraction = text.match(/^Required (\d+\/\d+), confirmed (\d+\/\d+)$/);
  if (fraction) {
    return locale === "zh"
      ? `要求 ${fraction[1]}，已确认 ${fraction[2]}`
      : `Diperlukan ${fraction[1]}, disahkan ${fraction[2]}`;
  }
  return text;
};
const fpTranslateTree = (root, locale) => {
  if (!root) return;
  const index = fpLocaleIndex(locale);
  if (index < 0) return;
  document.documentElement.lang = locale === "zh" ? "zh-CN" : locale === "ms" ? "ms" : "en";
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walker.nextNode())) {
    if (!node.parentElement || node.parentElement.closest("[data-fp-no-translate]")) continue;
    if (node.__fpLastTranslation !== undefined && node.nodeValue !== node.__fpLastTranslation) {
      node.__fpSourceText = node.nodeValue;
    } else if (node.__fpSourceText === undefined) {
      node.__fpSourceText = node.nodeValue;
    }
    const source = node.__fpSourceText;
    const trimmed = source.trim();
    const translated = fpTranslation(trimmed, locale);
    const desired = source.replace(trimmed, translated);
    node.__fpLastTranslation = desired;
    if (node.nodeValue !== desired) node.nodeValue = desired;
  }
  const attributes = ["placeholder", "title", "aria-label", "alt"];
  root.querySelectorAll("*").forEach(element => {
    if (element.closest("[data-fp-no-translate]")) return;
    for (const name of attributes) {
      if (!element.hasAttribute(name)) continue;
      const key = `__fpSource_${name}`;
      const lastKey = `__fpLastTranslation_${name}`;
      if (element[lastKey] !== undefined && element.getAttribute(name) !== element[lastKey]) {
        element[key] = element.getAttribute(name);
      } else if (element[key] === undefined) {
        element[key] = element.getAttribute(name);
      }
      const source = element[key];
      const translated = fpTranslation(source, locale);
      element[lastKey] = translated;
      if (translated !== source && element.getAttribute(name) !== translated) element.setAttribute(name, translated);
    }
  });
};
