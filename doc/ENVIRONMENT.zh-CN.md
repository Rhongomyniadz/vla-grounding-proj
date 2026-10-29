# 开发环境与跨电脑交接

[English](ENVIRONMENT.en.md) | [简体中文](ENVIRONMENT.zh-CN.md)

[项目架构](IMPLEMENTATION_PLAN.zh-CN.md#2-系统实现) | [每周指南](../weekly-plan/README.zh-CN.md) | [第 1 周学习指南](../weekly-plan/week-01.zh-CN.md)

本指南的安装、迁移、执行、诊断及证据审查全部由智能体负责，用户审阅可选。缺少目标访问时保持目标检查待完成，并继续不依赖它的实现。

## 当前验证边界

Windows x64 是编写代码的环境；另一台 RTX 5080 电脑上的 Ubuntu/WSL2 x86-64 是执行环境。两侧均要求 Python 3.12。开发侧检查通过，不能证明目标侧 CUDA、渲染、推理或视频播放正常。

目前已在 Windows 完成软件包安装，并通过真实命令行冒烟检查。依赖图已解析为 `uv.lock`，但解析成功不代表 Linux 软件包已经安装或成功执行。目标侧安装、EGL 渲染、检查点推理和 MP4 播放仍未验证。只有目标侧证据齐全，第 1 周才算完成。

## 依赖与可迁移文件

`pyproject.toml` 将轻量开发依赖与仅限 Linux 的 `runtime` 可选依赖分开。运行环境采用 LeRobot 0.6.1、hf-libero 0.1.4、来自 CUDA 12.8 软件源的 PyTorch 2.10.0 / torchvision 0.25.0，以及 TorchCodec 0.10.0。即使 CUDA 可用，TorchCodec 也必须匹配 PyTorch 版本。锁文件覆盖 Windows AMD64 和 Linux x86-64，其他架构不在本阶段支持范围内。

将源码树、`pyproject.toml`、`uv.lock`、`.python-version`、`configs/`、`tests/` 和文档同步到目标侧 Linux 文件系统中的检出目录，例如 `~/projects/vla-grounding-proj`。迁移尚未提交的工作时，也要包含新增文件。两台电脑分别重建 `.venv`、`.cache` 和 `.runtime`；这些目录已被忽略，其中包含平台相关二进制或绝对路径。`artifacts/` 保留在本机，或单独迁移所需证据。不要在 WSL 中执行 Windows 虚拟环境，也不要把它复制到目标侧。

应用配置不包含机器相关的绝对路径。快照清单和 LIBERO 配置在目标侧生成，有意记录其真实本地路径。两台电脑使用同一份源码和锁文件。不要通过复制过去的 Windows 解释器操作目标侧的活动虚拟环境。

## 每次访问运行电脑时的交接

十二个里程碑均使用此步骤，通过已有授权访问操作目标。无法访问时准备准确交接，在获得访问能力或完成不可避免的用户操作前保留执行待完成。下方命令覆盖第 1 周及第 2 周标准指令试点；清单执行器、训练及分析仍为后续工作。相关执行器能够自动记录来源之前，交接记录由智能体明确维护。

1. **在编码电脑准备。** 检查 `git status --short`、`git --no-pager diff` 和必需未跟踪文件。运行下方适用的开发检查。选择唯一交接标识，记录目标里程碑、配置路径、准确目标命令、预期输出和待完成运行检查。所有组件均由智能体实现，包括首次回合循环与检查逻辑。
2. **冻结可迁移源码快照。** 包含 `src/`、`tests/`、`configs/`、`pyproject.toml`、`uv.lock`、`.python-version`、`.gitignore`、`AGENTS.md`、`README.md`、`doc/`、`weekly-plan/` 及以后必需项目脚本。若有 Git 基础版本则记录它，并为每个包含文件记录相对路径和 SHA-256。仅 Git 版本无法标识未提交工作。新增未跟踪代码/配置属于快照；被忽略的环境、缓存、生成运行路径、数据集、检查点和运行输出不属于源码快照。不为迁移创建提交；只拉取 Git 或归档 HEAD 不包含当前未提交改动。
3. **在运行电脑复制并核对。** 通过可用文件迁移方式，复制到目标 WSL Linux 文件系统下单独且命名明确的源码目录。保留文件字节，使用前比较完整文件列表及哈希。Windows 的 `Get-FileHash -Algorithm SHA256 <file>` 和 Linux 的 `sha256sum <file>` 可逐文件核对。交接记录保存在运行产物旁。不要把新快照合并进正在运行的检出，也不要覆盖目标侧独有改动；先把这些改动带回编码电脑统一处理。
4. **准备目标环境。** 确认主机名、`pwd -P`、解释器、后端、配置和锁文件标识。首次访问按下方目标安装/检查顺序操作；源码/依赖变化后，根据迁移的锁文件同步目标项目环境，并执行受影响的最小真实检查。基础 LIBERO 与 LIBERO-plus 保持分离。在本机重建 `.runtime` 路径及资源链接；复制来的绝对路径是来源记录，不是可复用运行设置。
5. **按依赖顺序执行。** 先完成周计划目标检查，再启动大任务。同一次运行期间源码/配置保持不变，记录准确调用、运行标识、源码/锁文件/配置哈希、实际机器/后端、退出状态、标准输出/错误及预期与实际产物。本地修正代码后需要新交接快照及受影响目标检查。只恢复兼容且未变的运行规格；不要在同一运行标识下改变代码或条件。
6. **带回并检查证据。** 复制下表所需完整证据包，保留相对路径、文件列表及哈希；分析前核对接收完整性。原始报告保持不变，包括目标绝对路径。可迁移分析以本地运行根目录解析文件；已有报告使用目标路径时使用显式路径映射。不为读取结果导入仿真器。播放视频，检查错误和覆盖，核对快照标识后再更新双语清单。

| 材料 | 迁移与归属 |
| --- | --- |
| 源码、配置和共享锁文件 | 编码电脑 → 目标；经过审查的不可变交接快照 |
| `.venv`、`.cache`、`.runtime`、生成的 LIBERO 配置和链接 | 每次目标安装在本机重建/解析，绝不复制 Windows 环境 |
| 固定模型/数据/资源及派生训练副本 | 在目标下载/准备，保留版本、划分映射及哈希；普通审查不必带回大文件 |
| 结果、清单、JSON 诊断、相机图像、选定张量、日志、视频及覆盖 | 目标 → 编码电脑，保留同一运行标识与目录结构 |
| 适配器/检查点权重、优化器状态和处理流水线 | 在目标保留并校验标识；需要备份或复现时明确迁移，不复制活动训练目录 |

按里程碑返回证据：第 1 周机器清单和 CUDA/渲染/策略报告及图像/视频；第 2–3 周试点轨迹、重置比较和执行步数实测；第 4–6 周任务/状态目录、清单、真实回合结果、谓词检查及恢复/覆盖证据；第 7 周后端/变体/参考清单和试点图像；第 8–9 周划分映射、加载器比较、可训练参数和训练日志、检查点标识及重载执行；第 10 周验证选择和含覆盖的完整最终记录；第 12 周全新环境比较记录。某次审查只复制选定大轨迹/视频时，目标侧仍保留全量证据。最终分析仍需全部最终结果记录，审查时须取回实际使用的每个引用产物。

运行电脑不可用时，在本地准备源码、配置、预测和运行步骤，真实执行练习和目标检查保持待完成。返回证据缺失表示交接未完成。哈希不符时，在执行或分析前修正迁移，或明确标识为新快照。根据真实目标日志诊断安装/运行错误，并通过同一循环带回修正。

## 开发侧安装

使用真实的 Python 3.12 解释器，而不是尚未配置的 Windows Store 别名。如果已能使用 `uv`，在检出目录执行 `uv sync --locked --extra tools`。否则，仅在项目环境中引导安装已声明的工具：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install ".[tools]"
.\.venv\Scripts\uv.exe sync --locked --extra tools
```

引导安装将 uv 放入项目环境，后续锁定同步使版本与共享锁文件一致。这不会在 Windows 安装 Linux 的运行依赖。

从仓库根目录执行：

```powershell
.\.venv\Scripts\python.exe -m vla_grounding.authoring --config configs/week-01.json --output artifacts/authoring/check-01.json
.\.venv\Scripts\python.exe tests/smoke_authoring.py --config configs/week-01.json
.\.venv\Scripts\ruff.exe check src tests
.\.venv\Scripts\ruff.exe format --check src tests
```

报告使用排他创建，每次检查应选择新输出文件。命令冒烟测试使用真实临时文件和子进程，不模拟 CUDA 或仿真器。Windows 边界检查仅在 Windows 执行；其他机器仍检查开发侧行为、无效外部配置和报告保护。

这些检查覆盖当前轻量开发包。后续分析只有在项目配置及共享锁中声明所需依赖后，才可在此运行。JSON、图像和视频可在不安装机器学习运行栈时检查；`.npz`/张量检查需要实际加载依赖，否则在目标执行并返回摘要。不要为了分析导入而在编码电脑安装 Linux 运行依赖组。

## 目标侧安装：以下命令尚待验证

先完成第 1 周第 1 次学习中的目标电脑清单。以下是 Ubuntu 24.04、Python 3.12 的候选步骤。将下方示例检出路径替换为经过核对的交接目录。安装系统软件包前先记录实际发行版；如果 Ubuntu 版本不同，应审查差异。

```bash
sudo apt-get update
sudo apt-get install -y python3.12-venv build-essential ffmpeg libegl1 libgl1 libgles2 libglib2.0-0
cd ~/projects/vla-grounding-proj
python3.12 -m venv .venv
.venv/bin/python -m pip install '.[tools]'
.venv/bin/uv sync --locked --extra tools --extra runtime --no-dev
```

按照 [WSL 官方驱动说明](https://docs.nvidia.com/cuda/wsl-user-guide/index.html)使用 Windows 主机的 NVIDIA 驱动。Python 安装包携带 CUDA 运行库，此安装方式不要求安装 Linux NVIDIA 显示驱动。`uv.lock` 固定 Python 软件包，系统软件包和主机驱动仍需根据真实目标侧记录。以后将 LIBERO-plus 放在另一个环境中。

在目标侧仓库根目录按顺序执行下列阶段。同一次开发运行使用共同目录，重跑时选择新目录：

```bash
.venv/bin/vla-target-check --config configs/week-01.json --output artifacts/week-01/run-01/cuda.json
.venv/bin/vla-fetch-assets --config configs/week-01.json --output artifacts/week-01/run-01/assets.json
.venv/bin/vla-render-smoke --config configs/week-01.json --assets artifacts/week-01/run-01/assets.json --output-dir artifacts/week-01/run-01/render
.venv/bin/vla-policy-smoke --config configs/week-01.json --assets artifacts/week-01/run-01/assets.json --output-dir artifacts/week-01/run-01/policy
```

1. **CUDA 检查：** 拒绝其他平台、Windows 挂载目录中的检出、其他 GPU、低于配置要求的剩余存储，以及不可用的 CUDA。在指定 GPU 上执行矩阵乘法，保存解释器、内核、驱动、显存、存储和关键软件包信息。这只是 CUDA 门槛，不是第 1 周的完整验收。
2. **资源下载：** 下载仿真资源、策略权重与已保存的处理流水线，以及 VLM 配置和分词器文件。策略提交固定在 `configs/week-01.json` 中；其余初始引用先解析为完整提交哈希，再开始下载。同一运行重复使用生成的清单，不要再次解析 `main`。本次冒烟检查不需要示范数据集或额外 VLM 权重。此阶段访问网络，使用 Hub 进度条，对传输或 HTTP 错误进行有上限的重试并发出警告。
3. **渲染检查：** 在不加载策略的情况下重置新任务，查看 `image.png`（主相机）、`image2.png`（腕部相机）和 `observation.npz`。PNG 使用上游的 180 度方向修正，保存的原始图像数组保留仿真器原方向。该文件中的八维状态已由环境处理器构造，但尚未经过策略归一化。
4. **策略检查：** 保存 `prediction.npz`、`executed-actions.npz`、`smoke.mp4` 和 `smoke.json`。严格从本地快照加载完整检查点，使用已保存的归一化与分词设置，调用 LeRobot 的有步数上限的原生轨迹函数。执行动作前验证解码数值有限，写视频后完整解码。智能体仍须检查播放或渲染的视频帧，并记录审查：能解码不代表动作合理或方向正确。

共享配置明确列出冒烟任务、种子、图像尺寸、步数预算、控制频率、GPU 和下载引用。短步数预算仅用于检查接口，不是评估时限或任务成功率测量；不要把它用于正式研究的回合上限。

## 连接层与证据约定

`bootstrap.py` 在导入仿真器前设置 EGL、设备序号及独立的 `LIBERO_CONFIG_PATH`，以非交互方式写入兼容 JSON 的 YAML。hf-libero 0.1.4 的 `get_assets_path()` 会独立查找安装模块旁的资源，因此引导代码把固定快照链接到**项目虚拟环境**中的原生资源位置。它拒绝替换已有目录或指向其他快照的链接，不修改第三方 Python 代码。重建目标环境时重新生成这些文件，不要跨机器迁移。

完成引导后，运行连接层仅从本地快照加载，关闭 Hub 网络访问、遥测及外部实验追踪。完整 SmolVLA 检查点提供骨干权重；从固定的本地 VLM 配置初始化结构，可以避免重复下载骨干权重。保存的策略流水线保留状态归一化和动作反归一化；相机重命名映射明确列出，并与固定检查点的公共特征约定核对。

数据流为：原始 HWC uint8 相机批次与原生机器人状态 → LeRobot 图像转换及 LIBERO 方向/位姿处理 → 检查点重命名、分词、归一化 → SmolVLA 动作块 → 检查点动作解码 → 仿真器。公共状态和动作宽度分别为八和七；模型内部补齐和图像缩放由上游 SmolVLA 执行。

`prediction.npz` 包含两路原始相机、原生末端位置/四元数与夹爪位置、处理后的策略张量、归一化预测动作块及首个解码动作。随后命令重建仿真器，重置策略、处理流水线和采样种子，再调用上游轨迹函数；通过数值容差检查已保存首动作与实际执行首动作一致。`executed-actions.npz` 保存实际短轨迹动作。通过 `smoke.json` 可恢复指令、映射、动作设置、配置、版本、硬件及产物关系。这些是开发证据，不是实验结果或冻结的评估清单。

观测检查及标准指令回合循环已实现。检查工具使用运行环境已有 NumPy 依赖；轻量 Windows 项目环境不安装 Linux 运行栈，可迁移 NPZ 检查需要另行声明的分析环境。[代码指南](CODE_GUIDE.zh-CN.md)解释当前结构，并随每次实现同步更新。

## 第 1 周审查与第 2 周试点命令

第 1 周源码已补齐此前缺少的[观测检查工具](../src/vla_grounding/inspection.py)。相机/策略冒烟自动保存 `inspection.json`。在已安装 NumPy 的环境中可另做审查：

```bash
.venv/bin/vla-inspect-arrays --input artifacts/week-01/run-01/policy/prediction.npz --output artifacts/week-01/run-01/policy/inspection-review.json
```

[标准回合命令](../src/vla_grounding/episode.py)使用明确用例而非短冒烟上限，输入约定及队列/轨迹设计见[代码指南](CODE_GUIDE.zh-CN.md#第-1-周检查及第-2-周回合实现)。仅在真实第 1 周目标门槛通过后执行。三个输入是开发用例，目标解析状态证据仍待获得。

下列**仅目标侧命令尚未在此验证**。每条冒烟命令经真实子进程执行 `vla_grounding.episode`，审查返回动作块/动作/帧；输出目录须全新。

```bash
.venv/bin/python tests/smoke_episode.py --config configs/week-01.json --case configs/week-02-case-00.json --assets artifacts/week-01/run-01/assets.json --output-dir artifacts/week-02/run-01/pilot-00
.venv/bin/python tests/smoke_episode.py --config configs/week-01.json --case configs/week-02-case-01.json --assets artifacts/week-01/run-01/assets.json --output-dir artifacts/week-02/run-01/pilot-01
.venv/bin/python tests/smoke_episode.py --config configs/week-01.json --case configs/week-02-case-02.json --assets artifacts/week-01/run-01/assets.json --output-dir artifacts/week-02/run-01/pilot-02
```

直接命令约定：`vla-run-episode --config <config.json> --case <case.json> --assets <assets.json> --output-dir <fresh-directory>`。仅支持单个标准开发回合，无批处理模式、恢复或改变目标评分。

完成运行含 `episode.json`、状态记录、逐步 NPZ/JSON、完整预测块及视频。`request.json` 保留初始未完成内容不改写，仅最终结果标记完成。基础设施异常时保留请求/状态/转移及原错误，修正后在新目录重跑。超时是已完成但不成功的结果，不代表基础设施无效。

在已安装 NumPy/Pydantic 环境运行可迁移证据检查：

```bash
python tests/smoke_evidence.py --cases-dir configs
```

常规项目开发冒烟及 Ruff 检查在 Windows 通过；新增证据冒烟使用已有内置 Python 3.12 / NumPy 2.3.5 解释器及明确源码路径通过，不能验证目标锁中的 NumPy 构建、CUDA 或策略/仿真器集成。新依赖解析/下载在已配置 PyPI/PyTorch 地址超时，未替换版本约束、源或锁内容；`uv lock --check --offline` 验证现有锁有效。严格静态类型检查仍待可用配置工具，不宣称已通过。

## 排错与完成标准

| 问题 | 检查与修正 |
| --- | --- |
| Python 别名或解释器错误 | 找到 Python 3.12，查看 `sys.executable`，明确调用当前检出的环境。 |
| 锁解析或安装失败 | 保存完整报错，使用仓库中的锁文件及其支持平台，不要删除版本约束来制造安装成功。 |
| CUDA 错误 | 对照目标主机 `nvidia-smi`、WSL 发行版/内核和安装包 CUDA 版本；编写代码电脑的 GPU 与此无关。 |
| Hub 下载失败 | 保存仓库、版本、HTTP 状态/响应体和最终异常，修复连接或认证，再创建新运行清单或复用完整快照。 |
| LIBERO 配置或资源冲突 | 检查报错中的目标路径和链接版本；若属于其他安装，使用新的项目环境。 |
| EGL 或纯色相机错误 | 加载策略前检查 WSL GPU 暴露、EGL 系统库、设备选择及仿真资源，不替换渲染后端。 |
| 特征或处理流水线不匹配 | 对照本地检查点配置、两个处理流水线 JSON 和保存的映射，保留归一化状态文件。 |
| 首动作不一致 | 排查重置状态、采样种子与预处理，保留部分产物及错误，不称其为通过验证的数据流。 |
| MP4 错误 | 检查原始编码/解码异常及 PyAV/FFmpeg 安装，保留部分文件排查，重跑到新输出目录。 |

保存准确命令和失败信息。只有真实证据存在，才同步勾选相应双语周计划；除机器报告外，还要包含智能体记录的数据流图、已验证检查工具、张量解释和视频播放/帧审查记录。

来源：[LeRobot 0.6.1 发布包](https://pypi.org/project/lerobot/0.6.1/)、[hf-libero 0.1.4 发布包](https://pypi.org/project/hf-libero/0.1.4/)、[TorchCodec 兼容性](https://github.com/meta-pytorch/torchcodec/releases/tag/v0.10.0)、[固定检查点处理流水线](https://huggingface.co/lerobot/smolvla_libero/tree/a24f1f380461b665158d52acd140152c79e8b36d)。
