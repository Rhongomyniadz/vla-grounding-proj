# 设计选择与代码结构

[English](CODE_GUIDE.en.md) | [简体中文](CODE_GUIDE.zh-CN.md)

本指南解释当前所有项目自有模块及结构。每次实现变更由智能体同步维护两种语言。实验参数以[实施计划](IMPLEMENTATION_PLAN.zh-CN.md)为准，安装命令及证据迁移以[环境指南](ENVIRONMENT.zh-CN.md)为准，函数细节保留在英文文档字符串中。

**状态：** 第 1 周工程代码已存在，Windows 开发检查已通过；目标安装、CUDA、EGL、策略推理及视频视觉审查仍未验证。观测检查及标准指令单回合循环已实现；受控清单、替代目标评分、指标、数据准备及训练集成仍在计划中。下方形状为实现检查的预期约定，不是目标实测结果。

## 1. 设计选择

| 选择 | 理由与权衡 |
| --- | --- |
| 单一小型 `src/vla_grounding` 包 | 集中实验控制，不增加额外服务或提前抽象；未来按实际职责拆分。 |
| 分离 Windows 开发与 Linux 运行依赖 | 可迁移配置/检查无须仿真器和 GPU 栈；目标兼容性需要另做真实检查。 |
| 必填配置与项目本地环境 | 显式输入使运行可检查；共享锁记录解析，不证明目标安装成功。 |
| 校验记录及小函数 | Pydantic 校验外部记录，TypedDict 仅描述原生数据；转换用函数，有状态外部系统用类。模型类描述记录，不建立应用对象层级。 |
| 复用 LeRobot 处理器、加载及轨迹 | 保留归一化、分词、图像/位姿约定及动作队列；必须检查固定源码及真实特征，上游冒烟不是受控实验执行器。 |
| 一次解析引用，运行使用本地快照 | 不可变 SHA 标识模型/分词器/资源；下载需要网络，引导后离线，目标路径逐机器重建。 |
| 仿真导入前引导 | EGL 与 LIBERO 配置影响导入行为；资源链接只在项目环境内，拒绝安装冲突。 |
| 分离诊断预测与执行 | 检查动作块而不消耗队列；比较首动作前重建/重置仿真器、策略及随机数，尚不等于通用显式状态恢复。 |
| 保留证据，明确失败 | 独占创建输出避免覆盖，部分产物仅供诊断。网络传输/HTTP 失败有限重试并警告，配置/集成错误抛出。 |
| 隔离基础 LIBERO 和 LIBERO-plus | 二者共用导入命名空间；分支集成尚待实现，鲁棒性结论前须验证路径/导入及无扰动参考。 |
| 当前双语说明 | 用户可通过文档理解结构和决策；新增或变化结构同步更新指南，相互链接避免重复规格。 |

## 2. 仓库结构

| 位置 | 职责 |
| --- | --- |
| [pyproject.toml](../pyproject.toml) | 包元数据、依赖、命令入口、支持解析的平台及 Ruff 设置。 |
| [uv.lock](../uv.lock)、[.python-version](../.python-version) | 共享依赖解析及解释器选择；环境本地重建。 |
| [configs/week-01.json](../configs/week-01.json) | 可迁移开发冒烟输入：硬件、任务、相机/控制及请求资源引用。可变 VLM/资源引用在下载时解析后再运行；不是冻结实验清单。 |
| [src/vla_grounding/](../src/vla_grounding/) | 包实现，下文逐项说明。 |
| [tests/smoke_authoring.py](../tests/smoke_authoring.py) | 使用真实临时文件/子进程检查已安装命令，无伪造仿真器。 |
| [.gitignore](../.gitignore) | 环境、缓存、生成路径和产物不进入源码交接。 |
| [doc/](./)、[weekly-plan/](../weekly-plan/) | 当前双语设计/安装说明；智能体步骤、证据及用户每周代码/文档阅读清单。 |

### 记录与可迁移函数

| 源码与结构 | 输入、输出及关系 | 校验与设计理由 |
| --- | --- | --- |
| [config.py](../src/vla_grounding/config.py)：`WeekOneConfig` | 开发 JSON → 检查/连接层所需必填设置。 | strict/frozen Pydantic 记录约束任务、形状、控制、硬件和版本，忽略无关额外字段。 |
| `read_config(path)` | 文件 → 已校验 `WeekOneConfig`。 | 缺文件/字段或类型错误直接抛出，不猜测设置。 |
| [assets.py](../src/vla_grounding/assets.py)：`Snapshot` | 仓库 ID、不可变 40 字符 SHA、目标本地路径。 | 必填 strict/frozen 记录标识单个快照；读取资源包时检查目录存在。 |
| `AssetBundle` | 分别命名策略、VLM 和仿真器快照。 | 区分完整权重、分词器/VLM 元数据及仿真资源。 |
| `download_snapshot(repo_id, revision, repo_type, cache_dir, patterns)` | 明确 Hub 请求 → 解析 SHA 对应已下载 `Snapshot`。 | 先解析后下载，传输/HTTP 失败最多三次并结构化警告，最终抛出附请求上下文的最后错误；其他错误传播。 |
| `read_assets(path)` | 保存 JSON → 经校验且目录存在的 `AssetBundle`。 | 缺目标快照给出明确修正提示，不重新解析可变引用。 |
| [evidence.py](../src/vla_grounding/evidence.py)：`JsonValue`、`write_report(path, report)` | 递归 JSON 类型及映射 → 新 JSON 文件。 | 创建父目录、独占创建输出、拒绝 NaN/Infinity；保护旧证据，不实现实验恢复/覆盖逻辑。 |

### 命令入口与编排

每个 `main()` 接收明确必需路径，编排一项职责；准确调用见环境指南。

| 命令 / 源码 | 函数与行为 | 输出与边界 |
| --- | --- | --- |
| `vla-author-check` / [authoring.py](../src/vla_grounding/authoring.py) | `main()` → `check_authoring(config_path, output_path)`：要求 Python 3.12，校验配置并记录解释器/平台。 | 开发范围 JSON，`target_runtime_verified=false`；无 ML 导入或推理声明。 |
| `vla-target-check` / [runtime.py](../src/vla_grounding/runtime.py) | `main()` → `check_target(config, workspace)`；`require_target_platform(workspace)` 先要求 Linux/WSL2、支持架构/Python 及 Linux 文件系统；`check_target` 再查磁盘、LeRobot、CUDA/GPU 和真实矩阵乘法。 | 机器/包/驱动/CUDA 报告明确渲染和策略未验证，平台/设备/数值/命令错误抛出。 |
| `vla-fetch-assets` / [assets.py](../src/vla_grounding/assets.py) | `main()` 检查目标/输出、读取配置、下载仿真器、完整策略及选定 VLM 元数据/分词器。 | 新不可变 `AssetBundle` 清单，拒绝已有输出，大资源留在目标。 |
| `vla-render-smoke` / [render.py](../src/vla_grounding/render.py) | `main()` 检查目标/资源，运行导入前引导，重置并处理一条真实观测。 | 新目录两张朝向正确相机 PNG、`observation.npz`、`render.json`；不加载策略，`finally` 关闭仿真器。 |
| `vla-policy-smoke` / [smoke.py](../src/vla_grounding/smoke.py) | `main()` 检查目标/资源/引导，保存诊断预测，重建仿真器，调用有界上游 `rollout` 及处理器/解码器/视频回调。 | 预测/动作数组、MP4、JSON，检查有限动作及首动作一致；不测任务成功，视觉审查初始未完成。 |
| [__init__.py](../src/vla_grounding/__init__.py) | 包标记/文档字符串，无执行初始化或公共结构。 | 导入包不初始化 GPU/仿真器。 |

### 外部接口与原生数据结构

| 源码与结构 | 职责与约定 | 理由、校验及错误 |
| --- | --- | --- |
| [bootstrap.py](../src/vla_grounding/bootstrap.py)：`prepare_simulator(workspace, assets, cuda_device)` | 工作区、仿真快照、设备 → LIBERO 配置路径；设置 EGL、路径、离线及关闭追踪。 | 要求项目解释器、固定安装、完整资源且尚未导入仿真器；在项目环境链接资源并拒绝冲突。文件/环境变化是明确外部安装副作用。 |
| [simulator.py](../src/vla_grounding/simulator.py)：`FloatArray`、`EnvironmentObservation` | 原生浮点数组及处理后张量/文本映射别名。 | 明确上游公共类型，不另造格式；本模块需要运行依赖。 |
| `EndEffector`、`Gripper`、`RobotState`、`CameraViews`、`RawObservation` | 原生位置/四元数、夹爪、双相机和组合观测的 TypedDict。 | 描述必需字段，真实重置校验数组类型/形状/有限值；无关仿真字段归上游。 |
| `environment_config(config, episode_length)` | `WeekOneConfig` → 单任务上游 `LiberoEnv`，含显式相机映射、相对控制及长度上限。 | 复用厂商配置，当前仅基础 LIBERO。 |
| `require_camera(image, image_size)` | 原生相机及分辨率 → 校验或错误。 | 要求 uint8 批次形状，拒绝恒定图像，但不能检测全部视觉缺陷。 |
| `SimulatorConnector.__init__(config, episode_length)` | 创建单个同步向量环境及其处理器。 | 在外部边界管理仿真生命周期。 |
| `SimulatorConnector.reset(seed)` | 种子 → 上游重置后已校验原生观测。 | 检查双相机及有限位姿/夹爪；上游状态索引推进，显式状态恢复尚在计划中。 |
| `SimulatorConnector.prepare_observation(raw, instruction)` | 原生观测及明确文本 → LeRobot 处理后观测。 | 复用图像转换/旋转及位姿处理，要求有限八维公共状态。 |
| `SimulatorConnector.instruction()` | 环境 → 非空基准指令。 | 无效文本报错，后续语言用例必须传入自己的明确文本，保留有意空指令。 |
| `SimulatorConnector.close()` | 释放环境/EGL 资源。 | 正常结束及错误清理时由编排器调用。 |
| [policy.py](../src/vla_grounding/policy.py)：`ActionDecoder.__init__(processor)`、`ActionDecoder.__call__(action)` | 保存后处理器及归一化动作 → 解码 CPU 命令。 | 拒绝非有限输入，处理克隆，步进前要求有限 `(1, 7)` 输出。 |
| `PolicyConnector.__init__(assets, device)` | 本地快照及设备 → 严格完整模型和保存处理器。 | 校验公共特征、显式相机重命名、关闭发布并避免重复下载骨干，不兼容接口抛错。 |
| `PolicyConnector.prepare_observation(observation)` | 环境处理后数据 → 分词/归一化张量。 | 处理副本，校验必需图像/状态/词元/掩码形状及有限值；形状正确不能证明文本有意义且未截断。 |
| `PolicyConnector.predict_chunk(observation)` | 准备张量 → 有限归一化 `(1, chunk_size, 7)` 诊断块。 | 使用推理模式和输入副本，不消耗动作队列首动作。 |
| `PolicyConnector.reset()` | 清空模型队列/缓存及两个处理流水线。 | 回合间必须调用；调用方还控制随机数及仿真状态。 |
| [video.py](../src/vla_grounding/video.py)：`VideoRecorder.__init__(path, fps)` | 输出/FPS → 空帧缓冲记录器。 | 适配厂商渲染回调，缓冲适用于短冒烟，尚无长任务流式实现。 |
| `VideoRecorder.capture(env)` | 真实渲染回调 → 缓冲中 HWC RGB uint8 帧副本。 | 检查维数/通道/类型，复制防止后续仿真修改已保存帧。 |
| `VideoRecorder.save()` | 缓冲帧 → 新 MP4 和解码帧数。 | 要求多帧/新输出，用 LeRobot 写入并经 PyAV 解码全部帧，数量须一致；动作/朝向仍须另行视觉检查。 |

### 开发集成检查

[tests/smoke_authoring.py](../tests/smoke_authoring.py) 使用真实已安装命令及文件：

| 结构 | 职责 |
| --- | --- |
| `run_authoring(config, output, cwd)` | 用明确路径/超时，在检出目录外经真实子进程运行命令，返回进程结果。 |
| `check_cli_round_trip(config, directory)` | 要求诚实且成功的开发证据，随后重复输出必须失败且不覆盖原文件。 |
| `check_rejected_configuration(config, directory)` | 输入错误类型种子，要求字段明确错误、非零退出且不生成报告。 |
| `check_windows_boundary(config, directory)` | 真实 Windows 上要求目标命令在平台边界失败，不加载 ML。 |
| `main()` | 解析配置、创建临时文件、执行并报告检查，Windows 特定检查仅在 Windows 运行。 |

这些检查覆盖命令边界/证据保护，不能替代真实仿真器、策略、加载器或训练集成。

### 第 1 周检查及第 2 周回合实现

第 1 周审查发现缺少观测检查工具，目前已补齐源码与说明，并实现完整第 2 周标准指令试点。本地开发及可迁移证据检查通过；真实目标安装、第 1 周 GPU/相机/策略/视频门槛、第 2 周三个回合及真实错误清理检查仍未验证，当前无法访问目标。基础设施完成与行为成功是不同主张。

| 源码 / 结构 | 职责、约定与设计 |
| --- | --- |
| [inspection.py](../src/vla_grounding/inspection.py)：`EvidenceArray`、`ArrayInspection` | NumPy 证据别名及 strict/frozen 诊断记录，含名称、形状、类型、表示种类、数值范围、有限状态和掩码真值数。不导入仿真/模型，但需要已安装 NumPy。 |
| `inspect_array(name, value)` | 不修改数组，返回摘要。浮点必须有限，整数/词元单独报告范围，布尔掩码统计真值，文本无数值范围；空、object、复数数组明确报错。 |
| `inspect_arrays(arrays)`、`inspect_archive(path)` | 确定性排序摘要，禁止 pickle 加载真实 NPZ 并检查每个数组；空归档或不安全/无效内容失败，不生成成功报告。 |
| `write_inspection(source, output)`、`inspection.main()` | 独占写入 JSON；`vla-inspect-arrays --input ... --output ...` 接收明确路径。相机及策略冒烟现在自动生成 `inspection.json`。 |
| [episode_records.py](../src/vla_grounding/episode_records.py)：`EpisodeCase`、`StepSignals`、`EpisodeResult` | 可迁移 strict/frozen 输入、原生转移信号和完成试点结果。用例必需 ID、完整任务名、标准文本、明确初始状态索引、环境/策略种子及上限；结果含停止原因、成功、独立计数、耗时及产物引用。 |
| `read_case(path)`、`stop_reason(signals, steps, max_steps)` | 分配资源前校验外部 JSON。依次判断成功、原生终止、截断及明确超时，继续时返回无停止；步数错误报错。最后一步成功仍计成功。 |
| [simulator.py](../src/vla_grounding/simulator.py)：`environment_config(config, episode_length)`、`SimulatorConnector.__init__(config, episode_length)` | 明确回合长度，与第 1 周短冒烟上限分开；要求单个同步向量环境，终止观测在下一调用前保留。 |
| `SimulatorConnector.reset_case(case)` | 校验固定封装、标准任务/文本及初始状态表。公开 `init_state_id` 赋值前检查索引范围，避免上游取模替换。重置并拒绝目标已满足，返回选定/稳定后状态副本；任意保存状态恢复和可重复性审查仍属第 3 周。 |
| `SimulatorConnector.state_identity(states)` | 对各状态类型、形状及准确字节哈希，不能据此宣称数值可重复。 |
| `SimulatorConnector.reset(seed)`、`SimulatorConnector.validate_observation(raw)` | 重置两个环境处理器及计数，在重置和每步后校验相机/位姿/夹爪。 |
| `SimulatorConnector.step(action)` | 对解码动作副本应用环境后处理，校验后执行一次，返回原生终止观测、严格 `StepSignals` 及真实执行命令。要求固定 NEXT_STEP 路径的布尔成功/终止数组及有限奖励，不猜测成功或回退到其他 info 格式，统计真实执行次数。 |
| [policy.py](../src/vla_grounding/policy.py)：`RecordedSmolVLA`、`RecordedSmolVLA.reset()`、`RecordedSmolVLA._get_action_chunk(batch, noise, **kwargs)` | 固定 SmolVLA 的外部适配器。上游 `select_action` 调用受保护 `_get_action_chunk`，而不是公开 `predict_action_chunk`。只观察一次真实返回，校验完整动作块、复制到 CPU 并计数，保留上游队列及随机数行为。升级 LeRobot 时必须审查此版本耦合，拒绝 RTC。 |
| `PolicySelection`、`PolicyConnector.select_action(observation)` | 返回真实归一化队列动作、仅在实际预测时返回的新完整块，以及块编号/偏移。复制处理输入、统计选择调用、使用真实上游队列，不增加诊断预测。`PolicyConnector.reset()` 随模型/处理器重置全部计数。 |
| [trajectory.py](../src/vla_grounding/trajectory.py)：`save_arrays(path, arrays)` | 先校验再独占写入压缩 NPZ；object/非有限/空证据失败，已有文件不变。仅为单回合证据保存，不实现清单恢复。 |
| [evidence.py](../src/vla_grounding/evidence.py)：`source_hashes(workspace)` | 对当前 Python 源码、JSON 配置、包配置、解释器选择及依赖锁计算 SHA-256，含未提交/未跟踪源码。不创建提交，不替代完整交接步骤。 |
| [episode.py](../src/vla_grounding/episode.py)：`run_episode(config, case, assets, output)`、内部 `observation_arrays(raw)` | 管理完整同步试点，步进前复制观测避免向量缓冲复用。准备文本/张量、选择一次、解码一次、执行一次、录帧并先保存该步再继续。停止后不再步进/重置，校验独立计数/帧对齐、保存解码视频，在 `finally` 关闭仿真器。 |
| `episode.main()` | 解析明确配置/用例/资源/输出，真实目标检查和引导先于运行导入。独占创建运行，`request.json` 记录配置/目标/资源/源码标识，执行且证据保存、清理成功后才写 `episode.json`。异常保留原上下文及部分状态/转移证据，不生成完成记录或自动恢复。 |
| [tests/smoke_evidence.py](../tests/smoke_evidence.py)：`check_archives`、`check_cases`、`main()` | 真实 NPZ/JSON/子进程 I/O，覆盖掩码/文本、不改输入、拒绝覆盖、拒绝非有限、实际用例输入、停止优先级及 Windows 目标边界。数组仅为测试输入，不伪造机器人结果。 |
| [tests/smoke_episode.py](../tests/smoke_episode.py)：`audit_episode`、`main()` | 执行真实目标命令，逐步核对动作与来源预测块、帧索引、完成覆盖和预测次数。该集成检查已存在，但此处尚未运行。 |

三个[试点输入](../configs/week-02-case-00.json)选择固定 Spatial 任务 0 的索引 0、1、2，保留标准措辞。它们是开发输入，不是已解析/实测状态标识；目标须按实际固定数据核对任务/文本/索引。试点长度与 `WeekOneConfig.smoke_steps` 分离，不是冻结最终评估方案。

### 回合生命周期与产物对齐

1. 目标检查/引导先于仿真/策略导入；标准用例校验及状态保存先于策略分配。
2. 恢复指定基准索引，重置环境处理器，保留选定及稳定后状态，并检查目标未满足。
3. 重置策略/归一化器和采样种子，保存视频帧 0。
4. 转移 `i` 复制原始输入，保存处理张量及准确文本，选择队列动作一次、解码一次；仅真实新预测时保存完整块。
5. 环境动作处理后执行一次，保留终止标志/奖励、真实控制及下一原始观测，保存帧 `i+1`。
6. 保存转移 `i` 的 NPZ 和 JSON。停止判断只使用真实信号，终止后不调用下一次自动重置。
7. 保存/解码视频，要求 `帧数 = 动作数 + 1`；独立选择/执行计数须等于转移数，关闭仿真器后才发布完成。

| 产物 | 含义 |
| --- | --- |
| `request.json` | 不可变请求用例、配置、目标/资源及选定源码哈希，初始 `completed=false` 不改写。 |
| `initial-state.npz` / `state.json` | 选定稳定前状态、实际稳定后状态、用例及状态哈希。 |
| `chunks/NNNNNN.npz` | 每次真实模型调用的完整归一化预测，仅检查点执行步数进入队列。 |
| `transitions/NNNNNN.npz` | 步前原始观测副本、处理后策略张量、下一原始观测、归一化选择动作、解码动作及实际执行动作。 |
| `transitions/NNNNNN.json` | 准确文本、原生信号、推理耗时、块/偏移、数组链接及前后帧索引。 |
| `episode.mp4` / `inspection.json` | 解码数量核对视频及首转移数组检查，均不代表视觉审查或任务必然成功。 |
| `episode.json` | 已完成强类型结果，基础设施异常时不存在；超时或不成功终止仍可成为有效完成结果。 |

回合耗时计入循环内逐步证据写入，不计模型加载及最终视频编码。这是带记录的开发耗时，不是无插桩吞吐量基准。

真实选择前后同步 CUDA，推理时间包含预测证据复制。可分别识别队列选择和新预测，不发生第二次采样。当前环境后处理为恒等，目标审查核对解码/实际动作相等。改变目标、任意状态恢复、清单恢复、CSV 汇总及最终指标仍等待对应后续里程碑。

## 3. 数据流与控制流

可迁移路径：`authoring.main → read_config → check_authoring → write_report`。

运行路径：`read_config → check_target/require_target_platform → read_assets → prepare_simulator → 运行导入/连接层 → 操作 → 证据 → 清理`。资源下载是离线仿真前独立的联网阶段，引导须早于仿真器/OpenGL 导入。

1. 仿真重置返回原生相机批次及位置/四元数/夹爪分量。
2. 环境预处理转换图像布局/朝向和位姿，注入明确指令。
3. 策略预处理重命名相机、分词并应用保存归一化/设备处理。
4. 诊断预测提供归一化块，真实上游动作选择还管理动作队列。
5. 解码器反归一化并校验命令，上游轨迹步进环境。
6. 记录器保存真实帧，编排写数组/报告并释放资源。

| 阶段 | 当前单环境冒烟的预期约定 |
| --- | --- |
| 原始相机 | 两路 uint8 `(1, 256, 256, 3)`，`image` / `image2` |
| 原生机器人分量 | 位置 `(1, 3)`，四元数 `(1, 4)`，夹爪 `(1, 2)` |
| 公共状态 | 有限 `(1, 8)`，位姿转换说明其不等于原分量宽度之和 |
| 策略相机 | 两路 `(1, 3, 256, 256)`，重命名为 `camera1` / `camera2` |
| 语言 | 词元和注意力掩码 `(1, L)`，`L` 为检查点分词长度 |
| 预测块 | 有限归一化 `(1, T, 7)`，`T` 为检查点动作块容量 |
| 解码命令 | 有限 `(1, 7)` |

内部缩放/补齐归上游 SmolVLA，公共宽度不代表内部维度一致。主研究动作执行步数仍受实施计划控制。

冒烟保存预测及首个解码动作，随后重置策略/处理器、关闭并重建仿真器、重置随机数并运行上游轨迹。首个实际动作必须在 `rtol=1e-4` / `atol=1e-5` 内一致；不一致则抛错，排查状态/预处理/随机数。该比较已实现，但尚未在目标验证。

`smoke.json` 关联指令、配置、快照标识、重命名、动作块/执行步数及相对运行目录产物。`human_video_inspection_complete` 和 `task_success_measured` 初始为 false。保留原报告，以相同运行标识另存后续智能体视觉审查。MP4 可解码不能证明动作合理或成功。

## 4. 计划组件

以下职责尚无项目实现，不宣称未来路径/命令已存在。

| 里程碑 | 智能体实现 | 实现时必需说明 |
| --- | --- | --- |
| 3 | 任意状态恢复及重置/执行步数诊断 | 每个函数/记录、生命周期/停止、计数、可变状态、容差和真实轨迹 |
| 4–5 | 目录、用例、清单/执行器/恢复、目标评分 | 标识、配对、模板划分、谓词、旧目标终止、首目标并列、错误及产物 |
| 6 | 指标、分组 bootstrap、绘图 | 公式、分母、任务权重、保留配对、缺失覆盖及真实算例 |
| 7 | 隔离鲁棒性后端、变体及参考 | 导入/路径、真实元数据映射、采样及物理/视觉局限 |
| 8–9 | 划分/重标注、训练集成及启动/恢复 | 源数据链路、加载器等价、归一化、适配器/冻结参数、预算及重载证据 |
| 10 | 选择、最终冻结及覆盖 | 仅验证集规则/并列、不可变标识、重试与条件区别、缺失结果错误 |
| 11–12 | 分析/报告、产物审查及复现 | 可追踪主张、不确定性、失败证据、可迁移路径、差异及指南覆盖 |

实现后用真实源码链接替换计划项，并更新对应周阅读清单，列出用户应阅读的准确文件及符号。不得为填充文档而增加占位代码。

## 5. 维护与验收

每次变更列出源码模块/函数/类/记录，与双语指南逐项核对；在所属函数说明下解释非简单循环/分支，更新约定/理由/示例/状态，关联真实验证证据及源码/配置/锁标识。函数细节留在文档字符串，每个架构主题维护一对当前文档。

软件、证据、复现及文档仍是交付门槛。每周阅读清单明确用户应读懂的内容；智能体不等待用户亲自编码、手动执行或口头答辩。
