## :ant: Git Cycle

```shell
# 저장소를 로컬에 복제
$ git clone <주소> 
$ git pull origin master

# 기능 추가를 위해 branch 생성
$ git switch -c <브랜치 이름> # 브랜치 생성과 동시에 이동
$ git switch <브랜치 이름> # 브랜치로 이동

# 기능 구현후 원격 저장소에 브랜치 반영
$ git add .
$ git commit -m <커밋메시지>
$ git push origin <브랜치 이름>

# github에서 pull request 후 브랜치 삭제
$ git switch master
$ git branch -D branch_name
```

<br>

## :lemon: Git Flow

- master: 운영 서버로 배포하기 위한 브랜치
- django: 백엔드를 개발하는 브랜치
- vue: 프론트엔드를 개발하는 브랜치

<br>

## :ledger: Commit Convention

- Fix : 잘못된 동작을 고칠 때

  > Fix typo in Home.vue

- Add : 새로운 것을 추가할 때

  > Add Detail.vue

- Remove : 삭제가 있을 때

  > Remove Detail.vue

- Update : 정상적으로 동작하는 파일을 보완하는 경우

  > Update login logic to accounts.js