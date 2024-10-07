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
      <h1 class="welcome-message">Add Books</h1>
      
    </div>

    <div class="main-content" :class="{ animate: animateElements }" role="main">
      <div class="signup-form" role="form" aria-label="AddBooks Form">
        <div class="header">
          <h1>Uploads</h1>
        </div>
        <form @submit.prevent="submitbooks" enctype="multipart/form-data">
          <div class="mb-3">
            <label for="file" class="form-label">Upload File:</label>
            <input type="file" id="file" @change="handleFileUpload" class="form-control">
          </div>
          <br>
          <div class="mb-3">
            <label for="name" class="form-label">Name of book:</label>
            <input type="text" id="name" v-model="name" class="form-control" placeholder="Enter the name of the book">
          </div>
          <div class="mb-3">
            <label for="content" class="form-label">Description:</label>
            <input type="text" id="content" v-model="content" class="form-control" placeholder="Give a brief description">
          </div>
          <div class="mb-3">
            <label for="author" class="form-label">Author:</label>
            <input type="text" id="author" v-model="author" class="form-control" placeholder="Author's name">
          </div>
          <button type="submit" class="btn btn-info">Upload Book</button>
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
  name: 'AddBooks',
  props: ['id','username'],
  data() {
    return {
      isCollapsed: false,
      logo: require('@/assets/logo.jpg'),
      animateElements: false,
      name: '',
      author: '',
      content: '',
      file: null,
      message: '',
      success:false
    };
  },

  mounted() {
    this.triggerAnimation();
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed;
    },
    logout() {
      // Implement logout logic here
      console.log('Logging out...');
    },
    deleteAccount() {
      // Implement account deletion logic here
      console.log('Deleting account...');
    },
    triggerAnimation() {
      setTimeout(() => {
        this.animateElements = true;
      }, 100);
    },
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    async submitbooks() {
      try {
        const formData = new FormData();
        formData.append('file', this.file);
        formData.append('name', this.name);
        formData.append('author', this.author);
        formData.append('content', this.content);

        const response = await axios.post('http://localhost:5000/addbooks', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log('Book uploaded successfully:', response.data);
        this.clearForm();
        this.message = response.data.message;
        this.success = true;
      } catch (error) {
        if (error.response && error.response.status === 400) {
            this.message = ':) Book already exists!';
            this.success=false;
        } else {
          console.error('Error uploading book:', error);
        }
      }
    },
    clearForm() {
      this.name = '';
      this.author = '';
      this.content = '';
      this.file = null;
      this.message = '';
    }
  }
};
</script>

<style>
/* Add your styles here */
</style>
