import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  vus: 20,           // virtual users
  duration: '60s',   // test duration
};

export default function () {
  http.get('http://localhost:8080');
  sleep(0.1); // simulate some think time
}
