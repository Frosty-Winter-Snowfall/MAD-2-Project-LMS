<template>
  <div class="libd">
    <div :class="['sidebar', { collapsed: isCollapsed, animate: animateElements }]" role="navigation">
      <button class="toggle-btn" @click="toggleSidebar">
        <i class="fas fa-bars" aria-hidden="true"></i>
        <span v-if="isCollapsed" class="sr-only">Expand</span>
        <span v-else class="sr-only">Collapse</span>
      </button>
      <h1 class="sstyle" v-if="!isCollapsed">Sidebar</h1>
      <ul v-if="!isCollapsed">
        <li><router-link :to="`/ldashboard/${id}/${username}`">Dashboard</router-link></li>
        <li><router-link :to="{ path: '/bookmanagement', query: { id: id, username: username } }">Book Management</router-link></li>
        <li><router-link :to="{ path: '/sectionmanagement', query: { id: id, username: username } }">Section Management</router-link></li>
        <li><router-link :to="{ path: '/usermanagement', query: { id: id, username: username } }">User Management</router-link></li>
      </ul>
    </div>
    <div class="top" :class="{ animate: animateElements }">
      <div class="logo" :class="{ animate: animateElements }">
        <img :src="logo" alt="Logo">
      </div>
      <h1 class="welcome-message">Edit Book</h1>
    </div>

    <div class="main-content" :class="{ animate: animateElements }" role="main">
      <div class="signup-form" role="form" aria-label="EditBook Form">
        <div class="header">
          <h1>Edit Book</h1>
        </div>
        <form @submit.prevent="submitEditedBook" enctype="multipart/form-data">
        <div class="mb-3">
            <label for="file" class="form-label">Upload New File:</label>
            <input type="file" id="file" @change="handleFileUpload" class="form-control">
          </div>
          <br>
          <div class="mb-3">
            <label for="name" class="form-label">Name of Book:</label>
            <input type="text" id="name" v-model="newName" class="form-control" placeholder="Enter the new name of the Book">
          </div>
          <div class="mb-3">
            <label for="author" class="form-label">Author:</label>
            <input type="text" id="author" v-model="newAuthor" class="form-control" placeholder="Enter the author's name">
          </div>
          <div class="mb-3">
            <label for="content" class="form-label">Description:</label>
            <input type="text" id="content" v-model="newContent" class="form-control" placeholder="Give a brief description">
          </div>
          <button type="submit" class="btn btn-primary">Save Changes</button>
          <div v-if="message" class="alert" :class="{'alert-success': success, 'alert-danger': !success}">
        {{ message }}
      </div>
        </form>
      </div>
    </div>

    <div class="footer" :class="{ animate: animateElements }">
      <p>Contact Me: 22f3000877@ds.study.iitm.ac.in | Happy Reading!</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'EditBooks',
  props: ['bookId', 'id', 'username'],
  data() {
    return {
      logo: require('@/assets/logo.jpg'),
      animateElements: false,
      newName: '',
      newAuthor: '',
      newContent: '',
      file: null,
      message: '',
      success:false
    };
  },

  mounted() {
    console.log('bookId:', this.bookId);
    this.triggerAnimation();
    this.fetchBookDetails();
  },

  methods: {
    triggerAnimation() {
      setTimeout(() => {
        this.animateElements = true;
      }, 100);
    },

    async fetchBookDetails() {
      try {
        const response = await axios.get(`http://localhost:5000/book/${this.bookId}`);
        this.newName = response.data.book_name;
        this.newAuthor = response.data.book_author;
        this.newContent = response.data.book_content;
      } catch (error) {
        console.error('Error fetching book details:', error);
      }
    },

    handleFileUpload(event) {
      this.file = event.target.files[0];
    },

    async submitEditedBook() {
      try {
        const formData = new FormData();
        formData.append('book_name', this.newName);
        formData.append('book_author', this.newAuthor);
        formData.append('book_content', this.newContent);
        if (this.file) {
          formData.append('file', this.file);
        }

        const response = await axios.post(`http://localhost:5000/editbook/${this.bookId}`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log('Book edited successfully:', response.data);
        this.message = response.data.message;
        this.success = true;
      } catch (error) {
        console.error('Error editing book:', error);
        this.message = 'Error editing book.';
        this.success = false;
      }
    }
  }
};
</script>

<style>
/* Add your styles here */
</style>
