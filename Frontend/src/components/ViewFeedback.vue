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
      <h1 class="welcome-message">View Ratings</h1>
    </div>
    <div class="main-content" :class="{ animate: animateElements }" role="main">
      <div class="feedback-list" :class="{ animate: animateElements }">
        <h2>Ratings</h2>
        <table>
          <thead>
            <tr>
              <th>Consumer Name</th>
              <th>Book Name</th>
              <th>Ratings Content</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="feedback in feedbacks" :key="feedback.nid">
              <td>{{ feedback.consumer_name }}</td>
              <td>{{ feedback.book_name }}</td>
              <td>{{ feedback.feedback_content }}</td>
              <td>
              <div class="button-group">
                <button class="delete-button" @click="deleteFeedback(feedback.nid)">Ignore</button>
                <div v-if="message" class="alert" :class="{'alert-success': success, 'alert-danger': !success}">
                  {{ message }}
                </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="!feedbacks.length">
          <p>No Feedbacks.</p>
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
  name: 'ViewFeedback',
  props: ['id', 'username'],
  data() {
    return {
      isCollapsed: false,
      logo: require('@/assets/logo.jpg'),
      animateElements: false,
      feedbacks: []
    };
  },
  mounted() {
    this.triggerAnimation();
    this.fetchFeedbacks();
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
    async fetchFeedbacks() {
      try {
        const response = await axios.get('http://localhost:5000/seefeedback');
        this.feedbacks = response.data;
      } catch (error) {
        console.error('Error fetching feedbacks:', error);
      }
    },
    async deleteFeedback(nid) {
      try {
        await axios.delete(`http://localhost:5000/deletefeedback/${nid}`);
        this.fetchFeedbacks();
      } catch (error) {
        console.error('Error deleting feedback:', error);
      }
    }
  }
};
</script>

<style>
.feedback-list {
  background: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  transition: all 1s ease-out;
  opacity: 0;
  transform: translateY(20px);
}

.feedback-list.animate {
  opacity: 1;
  transform: translateY(0);
}

.feedback-list table {
  width: 100%;
  border-collapse: collapse;
}

.feedback-list thead {
  background: #f5f5f5;
}

.feedback-list th, .feedback-list td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ccc;
}

.feedback-list th {
  position: sticky;
  top: 0;
  background: #f5f5f5;
}

.feedback-list tbody {
  display: block;
  max-height: 400px; /* Set the desired height */
  overflow-y: auto;
}

.feedback-list tr {
  display: table;
  width: 100%;
  table-layout: fixed;
}

.feedback-list td {
  word-wrap: break-word;
}

.feedback-list button {
  margin-top: 10px;
}
</style>
