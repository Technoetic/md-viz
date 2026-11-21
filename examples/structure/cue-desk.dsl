workspace "NEON ENCORE" {
 model {
  caller = person "무대감독"
  desk = softwareSystem "큐 관리 시스템"
  lighting = softwareSystem "조명 콘솔"
  playback = softwareSystem "반주 재생기"
  caller -> desk "큐 선택"
  desk -> lighting "조명 큐 번호 전송"
  desk -> playback "재생 시작 신호"
 }
 views {
  systemContext desk EncoreContext {
   include *
   autoLayout tb
  }
  styles {
   element "Person" {
    background #572c50
    color #ffffff
   }
   element "Software System" {
    background #263657
    color #ffffff
   }
   relationship "Relationship" {
    color #64cfc7
   }
  }
 }
}
