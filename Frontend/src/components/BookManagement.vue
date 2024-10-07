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
        <li><router-link :to="{ path: '/sectionmanagement', query: { id: id, username: username } }">Section Management</router-link></li>
        <li><router-link :to="{ path: '/usermanagement', query: { id: id, username: username } }">User Management</router-link></li>
      </ul>
    </div>
    <div class="top" :class="{ animate: animateElements }">
      <div class="logo" :class="{ animate: animateElements }">
        <img :src="logo" alt="Logo">
      </div>
      <h1 class="welcome-message">Manage Books</h1>
    </div>

    <div class="main-content" :class="{ animate: animateElements }" role="main">
      <div class="lwelcome-card" :class="{ animate: animateElements }">
        <h2>Welcome Back, {{ username }}!</h2>
        <p>Let's manage Books together!</p>
        <ul>
          <li><router-link :to="{ path: '/addbookstos', query: { id: id, username: username } }">Add Books to Sections</router-link></li>
          <li><router-link :to="{ path: '/removebooksfroms', query: { id: id, username: username } }">Remove Books from Sections</router-link></li>
        </ul>
      </div>
       <div class="sinfo-blocks" :class="{ animate: animateElements }">
        <div class="sinfo-block" :class="{ animate: animateElements }">
          <h3>Edit Books</h3>
          <ul>
            <li v-for="book in books" :key="book.id">
        <h4>{{ book.name }}</h4>
        <p>{{book.author}}</p>
        <div class="button-group">
        <button class="edit-button" @click="navigateToEditBooks(book.id)">Edit</button>
        <div class="button-gap"></div>
        <button class="delete-button" @click="deleteBook(book.id)">Delete</button>
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
  name: 'BookManagement',
  props: ['id', 'username','bookId'],
  data() {
    return {
      isCollapsed: false,
      logo: require('@/assets/logo.jpg'),
      animateElements: false,
      books: [],
      bookToEdit: null,
      newBookName: '',
      message: '',
      success:false
    };
  },
  mounted() {
    this.triggerAnimation();
    this.fetchBooks();
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed;
    },
    async fetchBooks() {
      try {
        const response = await axios.get('http://localhost:5000/books');
        this.books = response.data;
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    },
    
    
    async deleteBook(bookId) {
      try {
        const response=await axios.post(`http://localhost:5000/deletebook/${bookId}`);
        this.message = 'Book deleted successfully!';
        this.fetchBooks();
        this.message = response.data.message;
        this.success = true;
      } catch (error) {
        console.error('Error deleting book:', error);
        this.message = 'Error deleting book.';
        this.success=false;
      }
    },
    triggerAnimation() {
      setTimeout(() => {
        this.animateElements = true;
      }, 100);
    },
    navigateToEditBooks(bookId) {
    this.$router.push({
      path: `/editbooks/${bookId}`,
      query: { id: this.id, username: this.username } });
    }
  }
};
</script>


<style>

</style>