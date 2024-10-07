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
      <h1 class="welcome-message">View Statistics</h1>
    </div>
    <div class="main-content" :class="{ animate: animateElements }" role="main">
      <div class="statistics-container">
        
        <div v-if="loading" class="loading">Loading...</div>
        <div v-else class="statistics">
          <div class="statistic-box bg-color1">
          <h2>Total Users</h2>
            <p>{{ statistics.total_users }}</p>
          </div>
          <div class="statistic-box bg-color2">
            <h2>Active Users</h2>
            <p>{{ statistics.active_users }}</p>
          </div>
          <div class="statistic-box bg-color3">
            <h2>Total Books</h2>
            <p>{{ statistics.total_books }}</p>
          </div>
          <div class="statistic-box bg-color4">
            <h2>Borrowed Books</h2>
            <p>{{ statistics.total_borrowed_books }}</p>
          </div>
          <div class="statistic-box bg-color5">
            <h2>All Sections</h2>
            <p>{{ statistics.all_sections }}</p>
          </div>
          <div class="statistic-box bg-color6">
            <h2>Notifications Pending</h2>
            <p>{{ statistics.total_notifications }}</p>
          </div>
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
  name: 'ViewStatistics',
  props: ['id', 'username'],
  data() {
    return {
      isCollapsed: false,
      logo: require('@/assets/logo.jpg'),
      animateElements: false,
      statistics: {},
      loading: true,
    };
  },
  mounted() {
    this.triggerAnimation();
    this.fetchStatistics();
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
    async fetchStatistics() {
      try {
        const response = await axios.get('http://localhost:5000/statistics');
        this.statistics = response.data;
      } catch (error) {
        console.error('Error fetching statistics:', error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>


<style>
.statistics-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.loading {
  font-size: 18px;
}

.statistics {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  width: 100%;
  max-width: 1200px;
  margin-top: 20px;
}

.statistic-box {
  flex: 1 1 calc(30% - 10px);
  background: #fff;
  border: 1px solid #ddd;
  padding: 20px;
  margin: 10px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.bg-color1 { background-color: #eddd9f; }
.bg-color2 { background-color: #f1aea7; }
.bg-color3 { background-color: #9ec6e1; }
.bg-color4 { background-color: #a6dcbc; }
.bg-color5 { background-color: #dca6b7; }
.bg-color6 { background-color: #b6a6dc; }
</style>
