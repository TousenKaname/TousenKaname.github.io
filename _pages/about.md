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

I am currently a Ph.D. student in the Department of System Engineering at <a href='https://www.stevens.edu/'>Stevens Institute of Technology</a>, under the supervision of Assistant Professor <a href='https://www.stevens.edu/profile/fliu22'>Feng Liu</a>. Prior to that, I received my master's degree from the School of Computer Science and Technology at <a href='https://english.ecnu.edu.cn/'>East China Normal University</a>, where I was supervised by Associate Professor <a href='https://faculty.ecnu.edu.cn/_s16/cl2_6128/main.psp'>Lei Chen</a>. I completed my undergraduate studies at the School of Software and the School of Economics and Management (minor) at <a href='https://www.tiangong.edu.cn/main.htm'>Tianjin Polytechnic University</a>. Additionally, I interned for one year with the <a href='https://github.com/uni-medical'>GMAI</a> team at  <a href='https://www.shlab.org.cn'>Shanghai Artificial Intelligence Laboratory</a>. My leader is <a href='https://scholar.google.com/citations?user=Z4LgebkAAAAJ&hl'>Junjun He</a>, and my mentor is <a href='https://scholar.google.com/citations?hl=zh-CN&user=UFBrJOAAAAAJ&view_op=list_works'>Jin Ye</a>. <img src="https://img.shields.io/endpoint?url={{ url | url_encode }}&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations"></a>.

<span class='anchor' id='-educations'></span>

# 🎓 Educations

<div class="edu-entry"><img src="images/sit.png" alt="SIT" class="edu-logo"><div>*2025.09 - Present*, Stevens Institute of Technology, New Jersey, USA.</div></div>

<div class="edu-entry"><img src="images/ecnu.svg" alt="ECNU" class="edu-logo"><div>*2022.09 - 2025.06*, East China Normal University, Shanghai, China.</div></div>

<div class="edu-entry"><img src="images/tgu.jpg" alt="TGU" class="edu-logo"><div>*2018.09 - 2022.06*, Tianjin Polytechnic University, Tianjin, China.</div></div>

<span class='anchor' id='-publications'></span>


# 📝 Publications 

---
<div class='paper-box'><div class='paper-box-image'><div><div class="badge">MICCAI 2024</div><img src='images/pub-sammed3d-moe.png' alt="sym" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

-	`Wang G*`, Ye J\*, Cheng J, et al. SAM-Med3D-MoE: Towards a Non-Forgetting Segment Anything Model via Mixture of Experts for 3D Medical Image Segmentation[J]. arXiv preprint arXiv:2407.04938, 2024. Accepted by MICCAI2024.
[[PDF]](https://arxiv.org/pdf/2407.04938) <span class='show_paper_citations' data='avkysggAAAAJ:9yKSN-GCB0IC'></span>

</div>
</div>

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">NeurIPS 2024</div><img src='images/pub-gmai-mmbench.png' alt="sym" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

-	Chen P\*, Ye J\*, `Wang G*`, et al. GMAI-MMBench: A Comprehensive Multimodal Evaluation Benchmark Towards General Medical AI[J]. arXiv preprint arXiv:2408.03361, 2024. Accepted by NeurIPS2024.
[[PDF]](https://arxiv.org/pdf/2408.03361) [[Homepage]](https://uni-medical.github.io/GMAI-MMBench.github.io/) <span class='show_paper_citations' data='avkysggAAAAJ:2osOgNQ5qMEC'></span>

</div>
</div>

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">CVPR 2025</div><img src='images/pub-slidechat.jpg' alt="sym" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

-	Chen Y\*, `Wang G*`, Ji Y\*, et al. SlideChat: A Large Vision-Language Assistant for Whole-Slide Pathology Image Understanding[J]. arXiv preprint arXiv:2410.11761, 2024. Accepted by CVPR2025.[[PDF]](https://arxiv.org/pdf/2410.11761)[[Homepage]](https://uni-medical.github.io/SlideChat.github.io/) <span class='show_paper_citations' data='avkysggAAAAJ:UeHWp8X0CEIC'></span>

</div>
</div>

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">Biomedical Signal Processing and Control</div><img src='images/pub-afd-polyp.jpg' alt="sym" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

-	Zou S\*, `Wang G*`, Zhang Y\*, et al. Adaptive feature decoupled network for polyp segmentation. Accepted by Biomedical Signal Processing and Control.[[PDF]](https://www.sciencedirect.com/science/article/pii/S1746809425008389?dgcid=coauthor) <span class='show_paper_citations' data='avkysggAAAAJ:YsMSGLbcyi4C'></span>

</div>
</div>

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">CVPR 2025</div><img src='images/pub-imis.jpg' alt="sym" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

-	Cheng, J., Fu, B., Ye, J., `Wang, G.`, Li, T., Wang, H., ... & He, J. (2024). Interactive Medical Image Segmentation: A Benchmark Dataset and Baseline. arXiv preprint arXiv:2411.12814.  Accepted by CVPR2025.[[PDF]](https://arxiv.org/pdf/2411.12814)[[Homepage]](https://uni-medical.github.io/IMIS-Benchmark/) <span class='show_paper_citations' data='avkysggAAAAJ:IjCSPb-OGe4C'></span>

</div>

</div>
<div class='paper-box'><div class='paper-box-image'><div><div class="badge">MICCAI 2025</div><img src='images/pub-ophora.jpg' alt="sym" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

-	Li, W., Hu, M., `Wang, G.`, Liu, L., Zhou, K., ... & He, J. (2024). Ophora: A Large-Scale Data-Driven Text-Guided Ophthalmic Surgical Video Generation Model. Accepted by MICCAI2025.[[PDF]](https://arxiv.org/pdf/2505.07449) <span class='show_paper_citations' data='avkysggAAAAJ:Y0pCki6q_DkC'></span>

</div>

</div>

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">MIA</div><img src='images/pub-f2tta.jpg' alt="sym" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

-	Wei Li, Jingyang Zhang, Lihao Liu, `Guoan Wang`, Junjun He, Yang Chen, Lixu Gu. F^2TTA: Free-Form Test-Time Adaptation on Cross-Domain Medical Image Classification via Image-Level Disentangled Prompt Tuning. Submitted to Medical Image Analysis.[[PDF]](https://arxiv.org/pdf/2507.02437) <span class='show_paper_citations' data='avkysggAAAAJ:W7OEmFMy1HYC'></span>

</div>
</div>

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">AAAI2026</div><img src='images/pub-gmai-vl.jpg' alt="sym" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

-	Tianbin Li, Yanzhou Su, Wei Li, Bin Fu, Zhe Chen, Ziyan Huang, `Guoan Wang`, et al. GMAI-VL & GMAI-VL-15M: Towards General Medical AI with a Large Vision-Language Model and a Comprehensive Multimodal Dataset.  Accepted by AAAI2026.[[PDF]](https://arxiv.org/pdf/2411.14522) <span class='show_paper_citations' data='avkysggAAAAJ:zYLM7Y9cAGgC'></span>

</div>
</div>

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">PRCV 2023</div><img src='images/pub-prfnet.jpg' alt="sym" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

-	Chen, J., Cheng, J., Jiang, L., Yin, P., `Wang, G.`, & Zhu, M. (2023, October). PRFNet: Progressive Region Focusing Network for Polyp Segmentation. In Chinese Conference on Pattern Recognition and Computer Vision (PRCV) (pp. 394-406). Singapore: Springer Nature Singapore. Accepted by PRCV2023.
[[PDF]](https://link.springer.com/chapter/10.1007/978-981-99-8469-5_31)] <span class='show_paper_citations' data='avkysggAAAAJ:d1gkVwhDpl0C'></span>

</div>
</div>

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">ICME 2023</div><img src='images/pub-sqt.jpg' alt="sym" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

- Huai, T., Yang, S., Zhang, J., `Wang, G.`, Yu, X., Ma, T., & He, L. (2023, July). SQT: Debiased Visual Question Answering via Shuffling Question Types. In 2023 IEEE International Conference on Multimedia and Expo (ICME) (pp. 600-605). IEEE. Accepted by ICME2023.
[[PDF]](https://ieeexplore.ieee.org/abstract/document/10219581)] <span class='show_paper_citations' data='avkysggAAAAJ:u-x6o8ySG0sC'></span>

</div>
</div>

<span class='anchor' id='-honors-and-awards'></span>

# 🏅 Honors and Awards
- Chinese National scholarship
- Tianjin Municipal People's Government Scholarship
- President's first scholarship
- H Award in the American Collegiate Mathematical Contest in Modeling
<!-- - Blue Bridge Cup C/C++ Group National Competition third prize -->
- Second prize of Asia-Pacific University Students Mathematical Contest in Modeling

<span class='anchor' id='-invited-talks'></span>

<!-- # 💬 Invited Talks
- *2021.06*, Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ornare aliquet ipsum, ac tempus justo dapibus sit amet.  -->

<span class='anchor' id='-internships'></span>

# 💻 Internships

- *2025.02 - 2025.06*, INTSIG	Information	Co.	Ltd.
- *2024.09 - 2024.11*, Shanghai Artificial Intelligence Laboratory.
- *2024.07 - 2024.08*, Nomura Information Technology Shanghai Co., Ltd (NTSH)
- *2023.12 - 2024.06*, Shanghai Artificial Intelligence Laboratory.
- *2023.09 - 2023.11*, Ubiquant Investment (Beijing) Corp.
- *2023.02 - 2023.06*, <a href="https://www.ilambda.com/About-us">iLambda</a> Corp.
