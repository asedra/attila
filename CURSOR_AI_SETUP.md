# Cursor AI Enterprise Setup Guide

Bu rehber, Cursor AI bilgi tabanına göre kapsamlı bir kurulum sağlar.

## 📋 **Kurulum Özeti**

### ✅ **Tamamlanan Konfigürasyonlar**

1. **🤖 MCP Server Entegrasyonları**
   - Jira ticket yönetimi
   - PostgreSQL veritabanı erişimi
   - Brave Search web arama
   - GitHub entegrasyonu
   - Slack bot entegrasyonu
   - File system erişimi

2. **🔧 Background Agent Yapılandırması**
   - Otomatik test çalıştırma
   - Dev server monitoring
   - Git workflow otomasyonu
   - Slack bildirimleri

3. **📋 Proje Yönetimi Kuralları**
   - Coding conventions
   - Project management rules
   - AI assistant guidelines

4. **💬 Slack Integration**
   - Team collaboration
   - Background agent kontrolü
   - PR review workflows
   - Monitoring alerts

5. **📊 Admin API Configuration**
   - Usage analytics
   - Team metrics
   - Spending reports
   - Quota management

6. **🔒 Security & Privacy**
   - Privacy Mode (strict)
   - SAML/SCIM authentication
   - Encryption at rest & in transit
   - Audit logging
   - Compliance (GDPR, SOX)

## 🚀 **Kurulum Adımları**

### 1. **Environment Variables**
```bash
cp environment-template.env .env
# .env dosyasını kendi değerlerinizle doldurun
```

### 2. **Cursor AI'da Proje Açma**
```bash
# Cursor AI'ı açın ve bu klasörü proje olarak açın
# .cursor/ konfigürasyonları otomatik yüklenecek
```

### 3. **MCP Server Aktivasyonu**
Cursor AI'da:
- `Tools` > `MCP Tools` menüsünden
- Configured tools listesini kontrol edin
- Her MCP server için "Connected" durumunu doğrulayın

### 4. **Background Agent Kurulumu**
```bash
# Cursor AI'da Background Agent'ı etkinleştirin
# Cursor > Background Agents > Configure
```

### 5. **Slack Entegrasyonu**
- Slack workspace'inize Cursor AI bot'unu ekleyin
- OAuth flow'u tamamlayın
- `#development` kanalında `@Cursor` test edin

## 🛠️ **Kullanım Örnekleri**

### **MCP Server Komutları**
```bash
# Jira ticket oluşturma
"@jira create a ticket for the authentication bug"

# PostgreSQL sorgusu
"@postgres show user table schema"

# Web arama
"@brave search for Node.js performance optimization"

# GitHub PR analizi
"@github analyze PR #123"
```

### **Background Agent Komutları**
```bash
# Slack'te kullanım
"@Cursor, fix the memory leak in user service"
"@Cursor, optimize the database queries"
"@Cursor, add tests for the new feature"
```

### **Admin API Kullanımı**
```bash
# Team metrics
curl -X GET https://api.cursor.com/teams/members -u your_api_key:

# Usage data
curl -X POST https://api.cursor.com/teams/daily-usage-data \
  -H "Content-Type: application/json" \
  -d '{"startDate": "2024-01-01", "endDate": "2024-01-31"}' \
  -u your_api_key:
```

## 📊 **Monitoring & Analytics**

### **Dashboard Metrics**
- Daily usage trends
- Model usage distribution
- Team productivity (acceptance rates)
- Cost analysis
- Performance metrics

### **Alerting**
- Usage threshold alerts
- Spending limits
- Error rate monitoring
- Security threat detection

## 🔒 **Security Best Practices**

### **Privacy Mode**
- Strict mode enabled
- No data retention
- Prompts deleted after response

### **Access Control**
- Role-based permissions
- MCP server approval required
- Background agent restrictions
- Admin API access control

### **Audit Logging**
- All activities logged
- 2-year retention
- SIEM integration
- Compliance reporting

## 🎯 **Gelişmiş Özellikler**

### **Max Mode Usage**
```bash
# Büyük codebase analizi için
"Analyze the entire codebase for performance issues"
"Refactor the authentication system across all files"
```

### **Composer Mode**
```bash
# Multi-file değişiklikler
"Implement user authentication across frontend and backend"
"Add logging to all API endpoints"
```

### **Memory System**
```bash
# Kararları hatırlatma
"Remember: We use binary search for efficiency in this project"
"Save this architectural decision for future reference"
```

## 🆘 **Troubleshooting**

### **MCP Server Bağlantı Sorunları**
```bash
# Konfigürasyonu kontrol et
cat .cursor/mcp.json

# API key'leri doğrula
echo $JIRA_API_KEY

# Bağlantı testi
curl -u $JIRA_USER_EMAIL:$JIRA_API_KEY $JIRA_INSTANCE_URL/rest/api/2/myself
```

### **Background Agent Sorunları**
```bash
# Environment konfigürasyonu
cat .cursor/environment.json

# Log'ları kontrol et
tail -f ~/.cursor/logs/agent.log
```

### **Slack Entegrasyon Sorunları**
```bash
# Bot token doğrula
curl -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
     https://slack.com/api/auth.test
```

## 📚 **Ek Kaynaklar**

- **Cursor Documentation**: https://docs.cursor.com
- **MCP Servers**: https://github.com/modelcontextprotocol/servers
- **Community Forum**: https://forum.cursor.com
- **Admin API Reference**: https://docs.cursor.com/admin-api

## 📞 **Destek**

Herhangi bir sorun yaşarsanız:
1. Bu dokümantasyonu kontrol edin
2. Cursor Community Forum'a başvurun
3. Support ticket açın

---

**🎉 Cursor AI Enterprise kurulumunuz tamamlandı!**

Bu kurulum ile şunlara sahip olursunuz:
- Tam otomatik geliştirme ortamı
- Güvenli ve compliance-ready yapı
- Kapsamlı monitoring ve analytics
- Team collaboration tools
- AI-powered development workflows

Happy coding with Cursor AI! 🚀 