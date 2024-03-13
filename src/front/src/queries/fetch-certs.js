import { ref, toRefs, reactive } from "vue";
import { useFetch } from "@q/";

const fetchCerts = () => {
    let resp = reactive({ response: [], error: null, fetching: false });
    const exec = async () => {
        const { response, error, fetchData, fetching } = useFetch(
            `/api/certs/all`,
            {}
        );
        fetchData();
        resp.response = response;
        resp.error = error;
        resp.fetching = fetching;
    };
    return { exec, ...toRefs(resp) };
};

export default fetchCerts;