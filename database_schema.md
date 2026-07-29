# 数据库表结构

数据库: MySQL, 表前缀如下

---

## 用户与认证

### `user`
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| name | String | 用户名 (unique) |
| email | String? | 邮箱 |
| email_verified | DateTime? | 邮箱验证时间 |
| image | String? | 头像 |
| password | String? | 密码 |
| created_at | DateTime | |
| updated_at | DateTime | |

### `account`
OAuth 账号关联。
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| user_id | String | → user.id |
| provider | String | OAuth 提供商 |
| provider_account_id | String | 提供商账号 ID |

### `session`
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| session_token | String | (unique) |
| user_id | String | → user.id |
| expires | DateTime | |

### `verificationtoken`
邮箱验证 token。

---

## 项目

### `projects`
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| name | String | 项目名 |
| description | Text? | 描述 |
| user_id | String | → user.id |
| created_at | DateTime | |
| updated_at | DateTime | |
| last_accessed_at | DateTime? | |

### `novel_promotion_projects`
小说推广项目配置，一对一关联 project。
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| project_id | String | → projects.id (unique) |
| art_style | String | 画风 (默认 american-comic) |
| video_ratio | String | 视频比例 (默认 9:16) |
| video_resolution | String | 视频分辨率 (默认 720p) |
| image_resolution | String | 图片分辨率 (默认 2K) |
| image_model | String? | 图片模型 |
| video_model | String? | 视频模型 |
| audio_model | String? | 语音模型 |
| character_model | String? | 角色图片模型 |
| location_model | String? | 场景图片模型 |
| storyboard_model | String? | 分镜图片模型 |
| edit_model | String? | 修图模型 |
| workflow_mode | String | 工作流模式 (默认 srt) |

---

## 角色

### `novel_promotion_characters`
项目角色。
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| novel_promotion_project_id | String | → novel_promotion_projects.id |
| name | String | 角色名 |
| aliases | Text? | 别名 |
| profile_data | Text? | 角色档案数据 |
| profile_confirmed | Boolean | 档案已确认 |
| introduction | Text? | 角色介绍 |
| voice_id | String? | 音色 ID |
| voice_type | String? | 音色类型 |
| source_global_character_id | String? | 来源全局角色 ID |

### `character_appearances`
角色外观（含生成的图片）。
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| character_id | String | → novel_promotion_characters.id |
| appearance_index | Int | 外观序号 (0=主外观) |
| change_reason | String | 变更原因 |
| description | Text? | 描述词 |
| descriptions | Text? | 描述词数组 (JSON) |
| image_url | Text? | 当前选中图片 URL |
| image_urls | Text? | 图片 URL 数组 (JSON) |
| selected_index | Int? | 当前选中图片索引 |
| previous_image_url | Text? | 上一次图片 |
| previous_image_urls | Text? | 上一次图片数组 |
| previous_description | Text? | 上一次描述词 |
| image_media_id | String? | → media_objects.id |
| created_at | DateTime | |
| updated_at | DateTime | |

> 唯一约束: [characterId, appearanceIndex]

---

## 场景

### `novel_promotion_locations`
项目场景。
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| novel_promotion_project_id | String | → novel_promotion_projects.id |
| name | String | 场景名 |
| summary | Text? | 场景描述 |
| asset_kind | String | 类型 (默认 location) |
| selected_image_id | String? | → location_images.id (当前选中图片) |
| source_global_location_id | String? | 来源全局场景 ID |

### `location_images`
场景图片。
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| location_id | String | → novel_promotion_locations.id |
| image_index | Int | 图片序号 |
| description | Text? | 描述词 |
| available_slots | Text? | 可用插槽 |
| image_url | Text? | 图片 URL |
| is_selected | Boolean | 是否选中 |
| previous_image_url | Text? | 上一次图片 |
| previous_description | Text? | 上一次描述词 |
| image_media_id | String? | → media_objects.id |

---

## 剧本 / 分镜

### `novel_promotion_episodes`
剧集。
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| novel_promotion_project_id | String | |
| episode_number | Int | 集号 |
| name | String | 集名 |
| description | Text? | 描述 |
| novel_text | Text? | 原文 |
| screenplay | Text? | 剧本 |
| audio_url | Text? | 音频 URL |
| srt_content | Text? | SRT字幕 |
| speaker_voices | Text? | 说话人音色配置 |

### `novel_promotion_clips`
片段（一集切分为多个 clip）。
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| episode_id | String | → episodes.id |
| start | Int? | SRT 起始 |
| end | Int? | SRT 结束 |
| duration | Int? | 时长 |
| summary | Text | 摘要 |
| location | Text? | 场景 |
| content | Text | 内容 |
| characters | Text? | 角色列表 |
| props | Text? | 道具列表 |
| screenplay | Text? | 剧本格式文本 |

### `novel_promotion_storyboards`
分镜（一对一关联 clip）。
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| episode_id | String | |
| clip_id | String | → clips.id (unique) |
| panel_count | Int | 面板数 (默认 9) |
| storyboard_image_url | Text? | 分镜总览图 |
| storyboard_text_json | Text? | 分镜文本 (JSON) |
| image_history | Text? | 图片历史 |
| photography_plan | Text? | 摄影计划 |

### `novel_promotion_panels`
面板（单张图）。
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| storyboard_id | String | → storyboards.id |
| panel_index | Int | 面板序号 |
| panel_number | Int? | 面板编号 |
| shot_type | Text? | 镜头类型 |
| camera_move | Text? | 镜头运动 |
| description | Text? | 描述 |
| location | Text? | 场景 |
| characters | Text? | 角色 |
| props | Text? | 道具 |
| image_prompt | Text? | 图片提示词 |
| image_url | Text? | 图片 URL |
| video_prompt | Text? | 视频提示词 |
| video_url | Text? | 视频 URL |
| video_generation_mode | Text? | 视频生成方式 |
| scene_type | String? | 场景类型 |
| acting_notes | Text? | 演技指导 |
| photography_rules | Text? | 摄影规则 |
| created_at | DateTime | |
| updated_at | DateTime | |

### `novel_promotion_shots`
镜头。
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| episode_id | String | |
| clip_id | String? | |
| shot_id | String | 镜头 ID |
| srt_start | Int | SRT 开始 |
| srt_end | Int | SRT 结束 |
| srt_duration | Float | 时长 |
| sequence | Text? | 序列描述 |
| locations | Text? | 场景 |
| characters | Text? | 角色 |
| plot | Text? | 剧情 |
| image_prompt | Text? | 图片提示词 |
| image_url | Text? | 图片 URL |

### `supplementary_panels`
补充面板。
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| storyboard_id | String | |
| source_type | String | 来源类型 |
| source_panel_id | String? | 来源面板 ID |
| description | Text? | |
| image_prompt | Text? | |
| image_url | Text? | |
| characters | Text? | |
| location | Text? | |

### `video_editor_projects`
视频编辑器项目。
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| episode_id | String | (unique) |
| project_data | Text | 剪辑数据 (JSON) |
| render_status | String? | 渲染状态 |
| render_task_id | String? | |
| output_url | Text? | |

---

## 语音

### `novel_promotion_voice_lines`
语音台词。
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| episode_id | String | |
| line_index | Int | 台词序号 |
| speaker | String | 说话人 |
| content | Text | 台词内容 |
| voice_preset_id | String? | 音色预设 |
| audio_url | Text? | 音频 URL |
| emotion_prompt | Text? | 情感提示 |
| matched_panel_index | Int? | 匹配面板序号 |
| audio_duration | Int? | 音频时长 |

### `voice_presets`
音色预设。
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| name | String | 名称 |
| audio_url | Text | 示例音频 |
| description | Text? | |
| gender | String? | |
| is_system | Boolean | 是否系统预设 |

---

## 任务

### `tasks`
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| user_id | String | |
| project_id | String | |
| episode_id | String? | |
| type | String | 任务类型 |
| target_type | String | 目标类型 |
| target_id | String | 目标 ID |
| status | String | queued/processing/completed/failed |
| progress | Int | 进度 0-100 |
| attempt | Int | 当前尝试次数 |
| max_attempts | Int | 最大尝试 (默认 5) |
| priority | Int | 优先级 (默认 0) |
| dedupe_key | String? | 去重键 (unique) |
| external_id | String? | 外部任务 ID |
| payload | JSON? | 请求参数 |
| result | JSON? | 结果 |
| error_code | String? | |
| error_message | Text? | |
| billing_info | JSON? | 计费信息 |
| queued_at | DateTime | |
| started_at | DateTime? | |
| finished_at | DateTime? | |
| heartbeat_at | DateTime? | |

### `task_events`
任务事件（用于 SSE 推送）。
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Int (auto) | 主键 |
| task_id | String | |
| project_id | String | |
| user_id | String | |
| event_type | String | created/processing/completed/failed |
| payload | JSON? | |
| created_at | DateTime | |

---

## 计费

### `user_balances`
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| user_id | String | (unique) |
| balance | Decimal(18,6) | 余额 |
| frozen_amount | Decimal(18,6) | 冻结金额 |
| total_spent | Decimal(18,6) | 总消费 |

### `balance_freezes`
余额冻结记录。
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| user_id | String | |
| amount | Decimal(18,6) | 冻结金额 |
| status | String | pending/committed/rolled_back |
| task_id | String? | 关联任务 |
| idempotency_key | String? | 幂等键 (unique) |
| expires_at | DateTime? | |

### `balance_transactions`
交易流水。
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| user_id | String | |
| type | String | charge/consume/refund |
| amount | Decimal(18,6) | 金额 |
| balance_after | Decimal(18,6) | 余额后 |
| description | Text? | |
| freeze_id | String? | 关联冻结 |
| project_id | String? | |
| episode_id | String? | |
| task_type | String? | |
| billing_meta | Text? | 计费详情 JSON |

### `usage_costs`
用量记录。
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| project_id | String | |
| user_id | String | |
| api_type | String | |
| model | String | |
| action | String | |
| quantity | Int | |
| unit | String | |
| cost | Decimal(18,6) | |

---

## 资产中心 (全局资产)

### `global_asset_folders`
资产文件夹（一层）。
| 字段 | 类型 |
|------|------|
| id | UUID |
| user_id | String |
| name | String |

### `global_characters`
全局角色。
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| user_id | String | |
| folder_id | String? | → folders.id |
| name | String | 角色名 |
| aliases | Text? | |
| profile_data | Text? | 角色档案 |
| voice_id | String? | 音色 ID |

### `global_character_appearances`
全局角色外观。
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| character_id | String | → global_characters.id |
| appearance_index | Int | |
| art_style | String? | |
| description | Text? | |
| image_url | Text? | |
| image_urls | Text? | |
| selected_index | Int? | |

### `global_locations`
全局场景。
| 字段 | 类型 |
|------|------|
| id | UUID |
| user_id | String |
| folder_id | String? |
| name | String |
| summary | Text? |

### `global_location_images`
全局场景图片。
| 字段 | 类型 |
|------|------|
| id | UUID |
| location_id | String |
| image_index | Int |
| image_url | Text? |

### `global_voices`
全局音色库。
| 字段 | 类型 |
|------|------|
| id | UUID |
| user_id | String |
| folder_id | String? |
| name | String |
| voice_id | String? |
| voice_type | String |

---

## 工作流执行 (Graph)

### `graph_runs`
工作流运行。
| 字段 | 类型 |
|------|------|
| id | UUID |
| user_id | String |
| project_id | String |
| workflow_type | String |
| status | String |
| target_type | String |
| target_id | String |
| input | JSON? |
| output | JSON? |

### `graph_steps`
工作流步骤。
| 字段 | 类型 |
|------|------|
| id | UUID |
| run_id | String |
| step_key | String |
| status | String |
| step_index | Int |

### `graph_step_attempts`
步骤尝试。
| 字段 | 类型 |
|------|------|
| id | UUID |
| run_id | String |
| step_key | String |
| attempt | Int |
| status | String |
| provider | String? |
| model_key | String? |
| input | JSON? |
| output_text | Text? |

### `graph_events`
工作流事件。
| 字段 | 类型 |
|------|------|
| id | BigInt (auto) |
| run_id | String |
| project_id | String |
| seq | Int |
| event_type | String |

### `graph_checkpoints`
工作流检查点。
| 字段 | 类型 |
|------|------|
| id | UUID |
| run_id | String |
| node_key | String |
| version | Int |
| state_json | JSON |

### `graph_artifacts`
工作流产物。
| 字段 | 类型 |
|------|------|
| id | UUID |
| run_id | String |
| artifact_type | String |
| ref_id | String |

---

## 媒体文件

### `media_objects`
统一媒体文件管理（MinIO/COS key 映射）。
| 字段 | 类型 |
|------|------|
| id | UUID |
| public_id | String (unique) |
| storage_key | String (unique) |
| sha256 | String? |
| mime_type | String? |
| size_bytes | BigInt? |
| width | Int? |
| height | Int? |
| duration_ms | Int? |

### `legacy_media_refs_backup`
媒体引用迁移备份。
| 字段 | 类型 |
|------|------|
| id | UUID |
| run_id | String |
| table_name | String |
| row_id | String |
| field_name | String |
| legacy_value | Text |

---

## 其他

### `user_preferences`
用户配置（API Key、模型选择等）。
| 字段 | 类型 |
|------|------|
| id | UUID |
| user_id | String (unique) |
| analysis_model | String? |
| character_model | String? |
| location_model | String? |
| video_model | String? |
| audio_model | String? |
| art_style | String |
| llm_base_url | String? |
| llm_api_key | Text? |
| fal_api_key | Text? |
| google_ai_key | Text? |
| ark_api_key | Text? |
| qwen_api_key | Text? |
| custom_models | Text? |
| custom_providers | Text? |
| image_concurrency | Int? |
| video_concurrency | Int? |

---

## 关系图

```
User ── Project ── NovelPromotionProject ── NovelPromotionCharacter ── CharacterAppearance
                                      ├── NovelPromotionEpisode ── NovelPromotionClip ── NovelPromotionStoryboard ── NovelPromotionPanel
                                      │                         └── NovelPromotionShot
                                      └── NovelPromotionLocation ── LocationImage
```

共计 **39 张表**。
