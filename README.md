我想用 Vue3 生成一个可以调用 REST API 的前端项目，需要和后端交互。
项目的功能：1.整个页面的最上方展示查询框，查询条件可以按奖金类型搜索，也可以根据总奖金的范围搜索，也可以同时搜索，然后点击查询按钮，查询结果用列表展示
2.查询框和查询按钮在同一行，查询结果用列表展示在下方
3.奖金类型字段：reward_categories， 总奖金字段：total_value_jpy
4.要展示的列表字段名称
{
  "event_name": 事件名称,
  "event_link": 链接,
  "status": 状态,
  "shop_id": 店铺id,
  "official_page": 官方网页,
  "start_time": 开始时间,
  "game_rule": 游戏规则,
  "entry_fee": 入场费,
  "prizes": 奖品,
  "prizes_original": 原始奖品,
  "address": 地址,
  "prefecture": 都道府県,
  "city_ward": 区,
  "tel": "03-6459-3286",
  "prizes_analyze": 奖品设计,
  "event_id": 事件id
}
5.请帮我生成完整的代码，包含HTML，CSS，JavaScript，VUE以及与后端交互部分  
