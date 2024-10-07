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

      </ul>
    </div>
    <div class="top" :class="{ animate: animateElements }">
      <div class="logo" :class="{ animate: animateElements }">
        <img :src="logo" alt="Logo">
      </div>
      <h1 class="welcome-message">Manage Users</h1>
    </div>

    <div class="main-content" :class="{ animate: animateElements }" role="main">
      <div class="lwelcome-card" :class="{ animate: animateElements }">
        <h2>Welcome Back, {{ username }}!</h2>
        <p>Let's manage Users together!</p>
        <ul>
          <li><router-link :to="{ path: '/issuerevoke', query: { id: id, username: username } }">Issue/Revoke Books to Users</router-link></li>
          <li><router-link :to="{ path: '/removebooksfroms', query: { id: id, username: username } }">Remove Books from Sections</router-link></li>
        </ul>
      </div>
       <div class="sinfo-blocks" :class="{ animate: animateElements }">
        <div class="sinfo-block" :class="{ animate: animateElements }">
          <h3>Edit Users</h3>
          <ul>
            <li v-for="user in users" :key="user.id">
        <span>{{ user.name }} ({{ user.active ? 'Active' : 'Inactive' }})</span>
        <div class="button-group">
        <button class="delete-button" @click="deleteUser(user.id)">Ban User</button>
        <div v-if="message" class="alert" :class="{'alert-success': success, 'alert-danger': !success}">
        {{ message }}
      </div>
        </div>
            </li>
          </ul>
        </div>
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
  name: 'UserManagement',
  props: ['id', 'username'],
  data() {
    return {
      isCollapsed: false,
      logo: require('@/assets/logo.jpg'),
      animateElements: false,
      users: [],
      message: '',
      success:false
    };
  },
  mounted() {
    this.triggerAnimation();
    this.fetchUsers();
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed;
    },
    async fetchUsers() {
      try {
        const response = await axios.get('http://localhost:5000/users');
        this.users = response.data;
      } catch (error) {
        console.error('Error fetching sections:', error);
      }
    },
    
    
    async deleteUser(userId) {
      try {
        const response=await axios.post(`http://localhost:5000/deleteuser/${userId}`);
        this.message = 'User banned successfully!';
        this.fetchUsers();
        this.message = response.data.message;
        this.success = true;
      } catch (error) {
        console.error('Error banning user:', error);
        this.message = 'Error banning user.';
        this.success=false;
      }

    },
    triggerAnimation() {
      setTimeout(() => {
        this.animateElements = true;
      }, 100);
    },
  }
};
</script>
<style>
</style>
