<template>
  <div id="notice-create">
    <div class="notice-title"><i class="far fa-sticky-note mr-3"></i>공지사항 작성</div>
    <div class="notice-body">
      <div class="reset">
        <v-btn color="error" outlined class="btns" @click="reset"><i class="fas fa-redo-alt mr-1"></i>다시 작성</v-btn>
      </div>
      <v-form ref="form" class="notice-create-form" v-model="valid" lazy-validation>
        <v-select v-model="select" :items="categorys" item-value="id" item-text="category" :rules="categoryRules"
          label="분류" required></v-select>
        <v-text-field v-model="title" :counter="30" :rules="titleRules" label="제목" required></v-text-field>
        <v-textarea v-model="content" :rules="contentRules" label="내용" class="mt-4" outlined></v-textarea>
        <v-btn :disabled="!valid" color="#607D8B" class="mr-4 btns text-light" 
          @click="noticeId !== undefined ? update() : write()">{{ noticeId !== undefined ? "수정" : "작성" }}
          <i class="fas fa-check-circle ml-1"></i></v-btn>
        <v-btn color="error" class="btns" @click="noticeId !== undefined ? updatecancel() : addcancel()">취소
          <i class="fas fa-times-circle ml-1"></i></v-btn>
      </v-form>
    </div>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "notice-create",
  data() {
    return {
      noticeId: "",
      select: null,
      title: "",
      content: "",
      writer_id: "",
      isNoticeAll: "",
      valid: false,
      categoryRules: [v => !!v || "분류를 선택해주세요"],
      titleRules: [
        v => !!v || "제목을 작성해주세요",
        v => (v && v.length <= 30) || "제목을 30자 이내로 작성해주세요",
      ],
      contentRules: [v => !!v || "내용을 작성해주세요"],
      categorys: [] // ["일반","중요","테마"]
    }
  },
  methods: {
    write() {
      if (this.$refs.form.validate()) {
        var noticeCreateForms = {
          "category": this.select,
          "title": this.title,
          "content": this.content,
          "writer": this.$store.getters.user_id,
          "isNoticeAll": 1
        }
        const requestHeader = this.$store.getters.requestHeader
        axios.post("/articles/theme_notice/", noticeCreateForms, requestHeader)
          .then(() => {
            this.$router.push({
              path: "/notice"
            })
          })
          .catch(err => {
            console.log(err)
          })
      }
    },
    update() {
      if (this.$refs.form.validate()) {
        var noticeUpdateForms = {
          "category": this.select,
          "title": this.title,
          "content": this.content,
          "writer": this.$store.getters.user_id,
          "isNoticeAll": this.isNoticeAll
        }
        const requestHeader = this.$store.getters.requestHeader
        axios.put(`/articles/theme_notice/${this.noticeId}/`, noticeUpdateForms, requestHeader)
          .then(() => {
            this.$router.push({
              path: `/notice/detail/${this.noticeId}`
            })
          })
          .catch(err => {
            console.log(err)
          })
      }
    },
    reset() {
      this.$refs.form.reset()
    },
    addcancel() {
      this.$router.push({
        path: "/notice"
      })
    },
    updatecancel() {
      this.$router.push({
        path: `/notice/detail/${this.noticeId}`
      })
    }
  },
  mounted() {
    this.noticeId = this.$route.params.noticeId
    const requestHeader = this.$store.getters.requestHeader
    axios.get("/articles/n_category/", requestHeader)
      .then(response => {
        this.categorys = response.data
      })
      .catch(err => {
        console.log(err)
      })
    if (this.noticeId !== undefined) {
      axios.get(`/articles/notices/${this.noticeId}/`)
        .then(response => {
          if (response.data.writer === this.$store.getters.user_id) {
            this.select = response.data.category
            this.title = response.data.title
            this.content = response.data.content
            this.writer_id = response.data.writer
            this.isNoticeAll = response.data.isNoticeAll
          } else {
            alert("수정 권한이 없습니다.")
            this.$router.push({
              path: "/notice"
            })
          }
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>

<style scoped>
  #notice-create {
    margin: 64px auto 0 auto;
    padding: 32px 0 48px 0;
    width: 100%;
    height: 100%;
    background-color: rgb(238, 240, 247);
  }

  .notice-title {
    font-family: "Cafe24Simplehae";
    font-size: 40px;
    margin: 0 auto 0 auto;
    width: 50%;
    border-radius: 7px 7px 0 0;
    box-shadow: 1px 1px 2px 1px rgb(100, 105, 109);
    background-color: rgb(255, 255, 255);
    padding: 2rem 0;
  }

  .notice-body {
    background-color: #fff;
    width: 50%;
    padding: 1.2rem 2rem;
    margin: 0 auto 0 auto;
    border-radius: 0 0 7px 7px;
    box-shadow: 1px 2px 2px 1px rgb(100, 105, 109);
  }

  .reset {
    text-align: right;
  }

  .btns {
    font-family: "Cafe24Simplehae";
    font-size: 18px;
  }

  .notice-create-form {
    padding: 2rem;
  }

  @media (max-width: 600px) {
    .notice-title {
      width: 95%;
    }

    .notice-body {
      width: 95%;
    }
    
    .notice-create-form {
      padding: 8px;
    }
  }
</style>
