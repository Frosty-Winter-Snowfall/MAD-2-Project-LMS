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
      <h1 class="welcome-message">Add Sections</h1>
    </div>

    <div class="main-content" :class="{ animate: animateElements }" role="main">
      <div class="signup-form" role="form" aria-label="AddSections Form">
        <div class="header">
          <h1>Uploads</h1>
        </div>
        <form @submit.prevent="submitsections" enctype="multipart/form-data">
          <div class="mb-3">
            <label for="name" class="form-label">Name of Section:</label>
            <input type="text" id="name" v-model="name" class="form-control" placeholder="Enter the name of the Section">
          </div>
          <div class="mb-3">
            <label for="content" class="form-label">Description:</label>
            <input type="text" id="content" v-model="content" class="form-control" placeholder="Give a brief description">
          </div>
          <button type="submit" class="btn btn-info">Upload Section</button>
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
  name: 'AddSections',
  props: ['id','username'],
  data() {
    return {
      isCollapsed: false,
      logo: require('@/assets/logo.jpg'),
      animateElements: false,
      name: '',
      content: '',
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
    triggerAnimation() {
      setTimeout(() => {
        this.animateElements = true;
      }, 100);
    },
    async submitsections() {
      try {
        const formData = new FormData();
        formData.append('name', this.name);
        formData.append('content', this.content);

        const response = await axios.post('http://localhost:5000/addsections', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log('Section uploaded successfully:', response.data);
        this.clearForm();
        this.message = response.data.message;
        this.success = true;
      } catch (error) {
        if (error.response && error.response.status === 400) {
            this.message = 'Section already exists or missing content!';
            this.success=false;
        } else {
          console.error('Error uploading Section:', error);
        }
      }
    },
    clearForm() {
      this.name = '';
      this.content = '';
      this.message = '';
    }
  }
};
</script>

<style>
/* Add your styles here */
</style>
