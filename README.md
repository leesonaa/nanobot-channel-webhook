# nanobot-channel-webhook

这是一个用于 Nanobot 的 Webhook 通道扩展。

## 安装步骤

1. 将项目下载或放到 `~/.nanobot` 目录下：

```bash
mv /path/to/nanobot-channel-webhook ~/.nanobot/nanobot-channel-webhook
```

2. 进入项目目录并安装为可编辑包：

```bash
cd ~/.nanobot/nanobot-channel-webhook
pip install -e .
```

3. 修改 `nanobot_channel_webhook/channel.py` 中的频道名和 `chat_id`：

- `channel` 字段填写你的频道名
- `chat_id` 可从运行日志中获取

4. 启动 Nanobot 并确认 Webhook 通道配置生效。

## config.json 示例

在你的 `config.json` 中加入或修改以下配置：

```json
"webhook": {
  "enabled": true,
  "port": 9000,
  "allowFrom": [
    "*"
  ]
}
```

## 说明

- 默认监听端口：`9000`
- 默认允许访问来源：`allowFrom` 配置为空时禁止访问

## 例子

```python
qq_msg = OutboundMessage(
    channel="wexin",
    chat_id="你的chatid",
    content=text,
    media=[],
    metadata={},
)
```
