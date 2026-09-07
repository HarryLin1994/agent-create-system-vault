---
type: source-intake-queue
status: active
tags: [inbox, raw-sources, ingestion, domain-retrieval]
reliability: medium
updated: 2026-09-07
---

# Source Intake Queue

## One-line Summary

Use this queue to tell the ingestion pipeline what domain a source batch belongs to and what expert behavior the sources should support.

## Current Batch

| Field | Value |
| --- | --- |
| Batch name | Evidence-Based Startup Methodology v0 |
| Domain | evidence-based-startup-methodology |
| Domain description | 證據導向創業方法論：從創業想法、customer discovery、MVP、商業模式、PMF、go-to-market 到是否 pivot / persevere 的執行方法。 |
| Target expert | 創業執行顧問。協助 founder 把想法拆成可驗證假設，設計客戶訪談與 MVP 實驗，判斷是否有 product-market fit，並根據證據決定下一步執行重點。 |
| Supported decisions | 是否值得開始做這個創業題目<br>目標客群與痛點是否足夠明確<br>MVP 應該做到什麼程度<br>要先驗證哪些商業模式假設<br>是否該 pivot、persevere 或繼續實驗<br>是否太早 scale team、product、sales 或 fundraising<br>下一個 1-2 週 sprint 應該做什麼 |
| Out of scope | 法律、稅務、會計、投資建議<br>保證募資成功、估值判斷或投資決策<br>替 founder 做最終商業決策<br>沒有客戶證據時直接判定產品一定會成功<br>高度監管產業的合規判斷，例如醫療、金融、保險 |
| Permission | needs-review |
| Sensitivity | mixed |
| Human reviewer | Harry Lin |
| Sensitivity handling | 公開創業方法論資料可直接使用。Founder notes、customer interview、pitch deck、財務模型、投資人回饋、客戶名單應視為 confidential。回答時避免暴露客戶姓名、公司內部數據、募資條件、未公開策略。 |
| Current source mode | user-provided local files only |
| Public source search | paused to avoid false-positive source judgments |
| Raw source folder | [[Raw Sources/evidence-based-startup-methodology/README|Raw Sources - Evidence-Based Startup Methodology]] |

## Priority Book Targets

| Book | Author | Priority | Processing Rule |
| --- | --- | --- | --- |
| The Lean Startup | Eric Ries | high | 可使用官方頁、出版社 metadata、合法 preview，或使用者提供且有權處理的檔案；不要自動下載未授權全文。 |
| Company of One: Why Staying Small Is the Next Big Thing for Business | Paul Jarvis | high | 可使用官方頁、出版社 metadata、合法 preview，或使用者提供且有權處理的檔案；不要自動下載未授權全文。 |
| The 4-Hour Workweek | Tim Ferriss | high | 可使用官方頁、出版社 metadata、合法 preview，或使用者提供且有權處理的檔案；不要自動下載未授權全文。 |

## Golden Questions Draft

Write questions the expert should answer after ingestion.

| Question | Expected source or note | Answerability |
| --- | --- | --- |
| 我有一個創業點子，還沒做產品，第一步應該驗證什麼？ | Steve Blank Customer Development、NSF I-Corps：先把假設拿到市場外部驗證，不要先埋頭開發 | supported |
| 我的 MVP 應該做到什麼程度才可以 launch？ | YC Essential Startup Advice、Lean Startup：launch early、MVP 用最小成本取得 validated learning | supported |
| 使用者說喜歡，但留存和付費都很弱，我該 pivot 還是繼續做？ | Lean Startup pivot/persevere、YC PMF 觀點：看真實行為、retention、willingness to pay，不只聽口頭喜歡 | supported |
| 我怎麼知道現在有沒有 product-market fit？ | YC、Strategyzer Value Proposition Canvas：看是否解決高痛點、是否有 pull、留存、重複使用、付費或強烈需求 | partial |
| 我們是不是太早 scale？ | YC 反對 premature scaling；CB Insights failure report 可作為風險來源：PMF 不足、現金耗盡、unit economics 不成立 | supported |

## Source Notes

- Put raw files in [[Raw Sources/evidence-based-startup-methodology/README|Raw Sources - Evidence-Based Startup Methodology]].
- Source manifests will be generated in [[Source Manifests/README|Source Manifests]].

## Related

- [[../07_Runbooks/Extract Expert Knowledge From Sources|Extract Expert Knowledge From Sources]]
- [[../09_Module-System/Domain Retrieval Modules/System Architecture - 12 Module Pipeline|System Architecture - 12 Module Pipeline]]
