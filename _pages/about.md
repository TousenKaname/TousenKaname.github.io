---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

{% if site.google_scholar_stats_use_cdn %}
{% assign gsDataBaseUrl = "https://cdn.jsdelivr.net/gh/" | append: site.repository | append: "@" %}
{% else %}
{% assign gsDataBaseUrl = "https://raw.githubusercontent.com/" | append: site.repository | append: "/" %}
{% endif %}
{% assign url = gsDataBaseUrl | append: "google-scholar-stats/gs_data_shieldsio.json" %}

<span class='anchor' id='about-me'></span>

Guoan Wang is a Ph.D. candidate in the Department of Systems Engineering at <a href='https://www.stevens.edu/'>Stevens Institute of Technology</a>, advised by Assistant Professor <a href='https://www.stevens.edu/profile/fliu22'>Feng Liu</a>. In Fall 2026, he will join <a href='https://newbrunswick.rutgers.edu/'>Rutgers University&ndash;New Brunswick</a> to continue his doctoral studies in Industrial and Systems Engineering. His research centers on artificial intelligence for healthcare, with particular interests in EEG foundation models and multimodal medical image analysis. He received his M.Eng. in Computer Technology from <a href='https://english.ecnu.edu.cn/'>East China Normal University</a>, advised by Associate Professor <a href='https://faculty.ecnu.edu.cn/_s16/cl2_6128/main.psp'>Lei Chen</a>, and his B.Eng. in Network Engineering, with a minor in Public Utilities Management, from <a href='https://www.tiangong.edu.cn/main.htm'>Tianjin Polytechnic University</a>. Prior to his doctoral studies, he spent a year as a research intern with the <a href='https://github.com/uni-medical'>GMAI</a> team at <a href='https://www.shlab.org.cn'>Shanghai Artificial Intelligence Laboratory</a>, working with <a href='https://scholar.google.com/citations?user=Z4LgebkAAAAJ&hl'>Junjun He</a> and <a href='https://scholar.google.com/citations?hl=zh-CN&user=UFBrJOAAAAAJ&view_op=list_works'>Jin Ye</a>. <img src="https://img.shields.io/endpoint?url={{ url | url_encode }}&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations&cacheSeconds=300">

<span class='anchor' id='-educations'></span>

# 🎓 Educations

<div class="edu-entry"><img src="images/logo-rutgers.png" alt="Rutgers" class="edu-logo"><div><em>2026.09 - Present</em>, Ph.D. in Industrial and Systems Engineering, Rutgers University, New Brunswick, New Jersey, USA.</div></div>

<div class="edu-entry"><img src="images/logo-sit.png" alt="SIT" class="edu-logo"><div><em>2025.09 - 2026.08</em>, Ph.D. Candidate in Systems Engineering, Stevens Institute of Technology, New Jersey, USA.</div></div>

<div class="edu-entry"><img src="images/logo-ecnu.svg" alt="ECNU" class="edu-logo"><div><em>2022.09 - 2025.06</em>, M.Eng. in Computer Technology, East China Normal University, Shanghai, China.</div></div>

<div class="edu-entry"><img src="images/logo-tgu.jpg" alt="TGU" class="edu-logo"><div><em>2018.09 - 2022.06</em>, B.Eng. in Network Engineering (minor in Public Utilities Management), Tianjin Polytechnic University, Tianjin, China.</div></div>

<span class='anchor' id='-publications'></span>


# 📝 Selected Publications

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">MICCAI 2024</div><img src='images/pub-sammed3d-moe.png' alt="sym" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

-	`Wang G*`, Ye J\*, Cheng J, Li T, Chen Z, Cai J, He J, Zhuang B. SAM-Med3D-MoE: Towards a Non-Forgetting Segment Anything Model via Mixture of Experts for 3D Medical Image Segmentation[J]. arXiv preprint arXiv:2407.04938, 2024. Accepted by MICCAI2024.
[[PDF]](https://arxiv.org/pdf/2407.04938) <span class='show_paper_citations' data='avkysggAAAAJ:9yKSN-GCB0IC'></span>

</div>
</div>

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">XXXX 2026</div><img src='images/pub-neuroweaver.png' alt="sym" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

-	`Wang G*`, Yang S\*, Ding J-E, Liu F. NeuroWeaver: An Autonomous Evolutionary Agent for Exploring the Programmatic Space of EEG Analysis Pipelines. Submitted to XXXX2026. [[PDF]](https://www.arxiv.org/pdf/2602.13473) <span class='show_paper_citations' data='avkysggAAAAJ:WF5omc3nYNoC'></span>

</div>
</div>

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">XXXX 2026</div><img src='images/pub-neuronarrator.png' alt="sym" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

-	`Wang G*`, Yang S\*, Ding J-E, Zhu H, Liu F. NeuroNarrator: A Generalist EEG-to-Text Foundation Model for Clinical Interpretation via Spectro-Spatial Grounding and Temporal State-Space Reasoning  Submitted to XXXX2026. [[PDF]](https://arxiv.org/pdf/2603.16880) <span class='show_paper_citations' data='avkysggAAAAJ:0EnyYjriUFMC'></span>

</div>
</div>

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">NeurIPS 2024</div><img src='images/pub-gmai-mmbench.png' alt="sym" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

-	Chen P\*, Ye J\*, `Wang G*`, Li Y, Deng Z, Li W, Li T, Duan H, Huang Z, Su Y, Wang B, Zhang S, Fu B, Cai J, Zhuang B, Seibel EJ, He J, Qiao Y. GMAI-MMBench: A Comprehensive Multimodal Evaluation Benchmark Towards General Medical AI[J]. arXiv preprint arXiv:2408.03361, 2024. Accepted by NeurIPS2024.
[[PDF]](https://arxiv.org/pdf/2408.03361) [[Homepage]](https://uni-medical.github.io/GMAI-MMBench.github.io/) <span class='show_paper_citations' data='avkysggAAAAJ:2osOgNQ5qMEC'></span>

</div>
</div>

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">CVPR 2025</div><img src='images/pub-slidechat.jpg' alt="sym" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

-	Chen Y\*, `Wang G*`, Ji Y\*, Li Y, Ye J, Li T, Hu M, Yu R, Qiao Y, He J. SlideChat: A Large Vision-Language Assistant for Whole-Slide Pathology Image Understanding[J]. arXiv preprint arXiv:2410.11761, 2024. Accepted by CVPR2025.[[PDF]](https://arxiv.org/pdf/2410.11761)[[Homepage]](https://uni-medical.github.io/SlideChat.github.io/) <span class='show_paper_citations' data='avkysggAAAAJ:UeHWp8X0CEIC'></span>

</div>
</div>

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">Biomedical Signal Processing and Control</div><img src='images/pub-afd-polyp.jpg' alt="sym" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

-	Zou S\*, `Wang G*`, Zhang Y\*, Shen Y, Yuan M, Su Y. Adaptive feature decoupled network for polyp segmentation. Accepted by Biomedical Signal Processing and Control.[[PDF]](https://www.sciencedirect.com/science/article/pii/S1746809425008389?dgcid=coauthor) <span class='show_paper_citations' data='avkysggAAAAJ:YsMSGLbcyi4C'></span>

</div>
</div>

<span class='anchor' id='-full-publications'></span>

# 📚 Full Publication List

<p class="gs-pub-note">This list is automatically synced from my <a href="https://scholar.google.com/citations?user=avkysggAAAAJ" target="_blank" rel="noopener">Google Scholar</a> profile<span id="gs-pub-updated"></span>.</p>

<div id="gs-pub-list"><p class="gs-pub-note">Loading publication list from Google Scholar…</p></div>

<span class='anchor' id='-academic-services'></span>

# 📖 Academic Services

**Journal Reviewer**
- Pattern Recognition
- Brain Informatics
- Frontiers in Radiology

**Conference Reviewer**
- The 29th International Conference on Medical Image Computing and Computer Assisted Intervention (MICCAI 2026)

<span class='anchor' id='-invited-talks'></span>

# 💬 Invited Talks

- *2026.03.27*, Rutgers University

<span class='anchor' id='-honors-and-awards'></span>

# 🏅 Honors and Awards
- Provost Doctoral Fellowship, Stevens Institute of Technology
- Chinese National scholarship
- Tianjin Municipal People's Government Scholarship
- President's first scholarship
- H Award in the American Collegiate Mathematical Contest in Modeling
<!-- - Blue Bridge Cup C/C++ Group National Competition third prize -->
- Second prize of Asia-Pacific University Students Mathematical Contest in Modeling

<span class='anchor' id='-internships'></span>

# 💻 Internships

- *2025.02 - 2025.06*, INTSIG	Information	Co.	Ltd.
- *2024.09 - 2024.11*, Shanghai Artificial Intelligence Laboratory.
- *2024.07 - 2024.08*, Nomura Information Technology Shanghai Co., Ltd (NTSH)
- *2023.12 - 2024.06*, Shanghai Artificial Intelligence Laboratory.
- *2023.09 - 2023.11*, Ubiquant Investment (Beijing) Corp.
- *2023.02 - 2023.06*, <a href="https://www.ilambda.com/About-us">iLambda</a> Corp.
