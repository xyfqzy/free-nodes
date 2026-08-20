# 免费节点订阅：Clash、V2RayN 与 Shadowrocket 使用说明

面向 Clash、V2RayN、v2rayNG 与 Shadowrocket（小火箭）的公开订阅目录。项目只维护两种容易识别、便于导入的订阅格式：**Base64 通用订阅** 与 **Clash YAML 订阅**。

> 项目主页：[nodes.udptoos.com](https://nodes.udptoos.com/) · 更新频率：每 2 小时 · 本仓库不承诺节点速度、稳定性或任何地区可用性。

## 订阅链接

| 格式 | 适用客户端 | 订阅链接 |
| --- | --- | --- |
| Base64（通用） | V2RayN、v2rayNG、Shadowrocket / 小火箭、支持 URI 订阅的客户端 | `https://nodes.udptoos.com/subscriptions/base64.txt` |
| Clash YAML | Clash Meta、Mihomo、Clash Verge、ClashX 等 YAML 配置客户端 | `https://nodes.udptoos.com/subscriptions/clash.yaml` |

所有条目会以 `🇭🇰HK - udptoos.com` 这类格式展示：国旗与两位国家缩写用于识别出口位置，`udptoos.com` 是统一显示名称。相同国家可能附带序号，以避免客户端中的重名冲突。

## 如何导入订阅

### Clash 节点 / Clash 订阅

1. 复制 Clash YAML 链接。
2. 在 Clash Meta、Mihomo、Clash Verge 或 ClashX 的「Profiles / 配置订阅」中添加 URL。
3. 下载或更新配置后选择该配置文件。

Clash YAML 是完整配置格式，不应作为 Base64 订阅导入。

### V2RayN 节点

1. 复制 Base64 通用订阅链接。
2. 在 V2RayN 中打开「订阅分组」，添加订阅 URL。
3. 点击更新订阅，再从服务器列表选择节点。

### Shadowrocket / 小火箭节点

1. 复制 Base64 通用订阅链接。
2. 在 Shadowrocket 点击右上角加号，选择 **Subscribe**。
3. 粘贴 URL 并完成添加，之后从订阅列表更新。

不同客户端版本的菜单文字可能略有不同；无法导入时，请优先检查订阅格式是否选对。

## 节点命名与 GEO 信息

节点名称按出口 IP 的公开地理归属生成国家缩写与国旗。例如 `🇭🇰HK - udptoos.com` 代表该节点解析到的 IP 归属为香港（HK）。地理数据库存在滞后或误差，国家信息仅用于筛选与识别，不代表服务提供者、线路质量或真实物理位置。

## 数据来源与检测方式

每两小时自动读取以下公开订阅源，并生成本仓库的两种统一输出：

- Clash / Standard：`https://raw.githubusercontent.com/kooker/FreeSubsCheck/main/all.yaml`
- Base64 通用：`https://raw.githubusercontent.com/kooker/FreeSubsCheck/main/base64.txt`

发布前会执行：

1. 解析可识别的 `vmess`、`vless`、`ss`、`trojan` URI；
2. 移除空记录，生成统一 Base64 订阅；
3. 校验 Clash 文档含有 `proxies` 列表；
4. 解析节点主机并根据公开 IP 地理数据统一命名。

这属于**格式与数据完整性校验**，不是速度测试、可用性测试或安全认证。公共节点的连通性会随时间、网络和地区变化。

## 常见问题

### 免费节点订阅为什么会失效？

上游公开节点会被关闭、限流或改变配置；因此请在客户端中定期更新订阅，并不要把公共节点用于账号登录、支付或其他敏感数据。

### Clash、V2RayN 和小火箭该使用哪个链接？

优先按客户端选择：Clash / Mihomo 使用 Clash YAML；V2RayN 与 Shadowrocket 使用 Base64 通用链接。

### 为什么名称后缀都是 udptoos.com？

这是项目的统一展示名称，避免向用户展示杂乱或可能误导的上游备注。实际地址、端口、协议和传输参数不会因显示名称而变化。

### 这个项目是机场吗？

不是。项目不销售服务、不提供账号，也不保证节点可用性；它只是整理公开订阅格式与客户端导入说明。

## 使用与安全提示

- 请遵守所在地法律、网络规则及服务条款。
- 公共节点不适合敏感账号、支付、个人资料或机密文件传输。
- 请自行判断来源、风险与客户端安全设置。
- 如发现格式问题，请通过 [Issues](https://github.com/xyfqzy/free-nodes/issues) 提交可复现信息。

## SEO 与站点入口

仓库首页与 [nodes.udptoos.com](https://nodes.udptoos.com/) 使用一致的订阅入口。站点包含 canonical、结构化数据、robots.txt 与 sitemap.xml，方便搜索引擎理解页面用途；内容聚焦 Clash 节点、V2RayN 节点、Shadowrocket 节点和免费订阅的实际导入流程，而非承诺无法验证的“高速”或“稳定”。

