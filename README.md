# SIEVE — ICLR 2027 论文

论文标题：**Not All Errors Matter: Semantic-Aware Silent Data Corruption Detection for Large Language Models**。

## 文件组织

`main.tex` 是唯一的论文编译入口，保留导言区、标题和作者信息、章节顺序、参考文献命令及附录编号设置。各章节通过 `\input` 引入；修改章节时直接编辑对应文件即可，无须复制导言区。

| 正文内容 | 文件 |
| --- | --- |
| 摘要 | `sections/abstract.tex` |
| Introduction | `sections/introduction.tex` |
| Design Motivation | `sections/design_motivation.tex` |
| SIEVE Design | `sections/sieve_design.tex` |
| Experiments | `sections/experiments.tex` |
| Related Work | `sections/related_work.tex` |
| Conclusion | `sections/conclusion.tex` |
| AI use statement | `sections/ai_use_statement.tex` |
| Ethics statement | `sections/ethics_statement.tex` |
| Reproducibility statement | `sections/reproducibility_statement.tex` |
| Acknowledgments | `sections/acknowledgments.tex` |

| 附录内容 | 文件 |
| --- | --- |
| Dataset and Evaluation-Scope Statistics | `appendices/dataset_statistics.tex` |
| Implementation Details | `appendices/implementation_details.tex` |
| Configuration Selection | `appendices/configuration_selection.tex` |
| Component Ablation Details | `appendices/component_ablation.tex` |
| Configuration-Matched Method Comparison | `appendices/method_comparison.tex` |
| Online Overhead Details | `appendices/online_overhead.tex` |
| Detector Transfer | `appendices/detector_transfer.tex` |
| Limitations | `appendices/limitations.tex` |

其他文件：

- `references.bib`：论文参考文献。
- `Figures/`：图片；章节内的图片路径仍相对于仓库根目录。
- `math_commands.tex`：共用数学命令。
- `iclr2027_conference.tex`：会议模板示例，不是论文编译入口。
- `SIEVE.pdf`：仓库已有的论文 PDF；修改源码后需重新编译才能更新。
- `scripts/`：现有绘图脚本。

## 编译

在仓库根目录执行以下命令（需要安装带有所需宏包的 TeX Live 或 MiKTeX，以及 `latexmk`）：

```sh
latexmk -pdf main.tex
```

也可以按顺序执行：

```sh
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

输出为 `main.pdf`。在 Overleaf 中，将 Main document 设置为 `main.tex`。

## GitHub 协作

1. 开始修改前同步远端 `main`，为本次修改建立独立分支。
2. 优先修改自己负责的章节文件；小节、图表及其说明保留在所属章节中。
3. 保持现有 `\label` 和引用键稳定，新增标签时避免重名。新增文献统一写入 `references.bib`。
4. 从仓库根目录编译 `main.tex`，检查交叉引用、参考文献和版面后，再提交并发起 Pull Request。
5. 调整章节顺序或增加章节时，更新 `main.tex` 中的 `\input` 列表及本说明。

本次拆分仅调整源码组织，未修改论文内容、章节顺序、图表路径或引用标签。
