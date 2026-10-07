import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;
import java.util.Set;
import org.yaml.snakeyaml.Yaml;

/** Parse the distributed YAML with ServerCore's actual bundled SnakeYAML. */
public class ServerCoreConfigCheck {
    static Object at(Map<?, ?> map, String... path) {
        Object value = map;
        for (String key : path) value = ((Map<?, ?>) value).get(key);
        return value;
    }
    static void expect(Object actual, Object expected) {
        if (!expected.equals(actual)) throw new IllegalArgumentException("Unexpected configuration: " + actual);
    }
    public static void main(String[] args) throws Exception {
        Yaml yaml = new Yaml();
        Map<?, ?> config = yaml.load(Files.readString(Path.of(args[0])));
        for (String section : new String[]{"dynamic", "breeding-cap", "activation-range"})
            expect(at(config, section, "enabled"), false);
        expect(at(config, "dynamic", "default-values"), Map.of());
        expect(at(config, "dynamic", "dynamic-settings"), java.util.List.of());
        for (String option : new String[]{"prevent-enderpearl-chunkloading", "chunk-tick-distance-affects-random-ticks", "prevent-moving-into-unloaded-chunks"})
            expect(at(config, "features", option), false);
        expect(at(config, "features", "lobotomize-villagers", "enabled"), false);
        expect(at(config, "features", "xp-merge-fraction"), 40);
        expect(at(config, "features", "xp-merge-radius"), 0.5);
        expect(at(config, "features", "item-merge-radius"), 0.5);
        Map<?, ?> spawning = (Map<?, ?>) config.get("mob-spawning");
        expect(spawning.keySet(), Set.of("zombie-reinforcements", "nether-portal-randomticks", "monster-spawners", "infested"));
        for (Object key : spawning.keySet()) expect(at(spawning, key.toString(), "enforce-mobcap"), false);
        Map<?, ?> opt = yaml.load(Files.readString(Path.of(args[1])));
        expect(opt, Map.of("reduce-sync-loads", false, "cache-ticking-chunks", true,
                          "optimize-command-blocks", false, "fast-biome-lookups", false,
                          "cancel-duplicate-fluid-ticks", false));
        System.out.println("ServerCore YAML: distances, mobcaps and behavior overrides disabled");
    }
}
