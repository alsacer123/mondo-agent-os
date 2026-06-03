# 安全边界

公开模板必须默认安全。

## 不要写进知识库

- API key
- token
- 密码
- 私钥
- 服务器 IP
- 完整 SSH 登录命令
- 客户姓名、手机号、微信、身份证、地址
- 未脱敏合同和报价
- 私人聊天记录
- 真实财务账户信息

## 推荐写法

可以记录变量名或占位符：

```text
OPENAI_API_KEY
GITHUB_TOKEN
YOUR_SERVER_ALIAS
YOUR_EXTERNAL_WORKSPACE_PATH
```

不要记录明文值。

## 外部工作区

大文件和敏感文件建议放到知识库之外，例如：

```text
external-workspace/
  outputs/
  cache/
  source-media/
  private/
```

知识库里只记录路径摘要和处理结论。

## 公开前检查

发布到 GitHub 前，至少搜索这些关键词：

```text
key
token
password
secret
ssh
http
https
手机号
微信
身份证
私钥
```

