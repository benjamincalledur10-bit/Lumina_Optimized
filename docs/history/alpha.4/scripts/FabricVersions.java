import java.io.BufferedReader;
import java.io.InputStreamReader;
import net.fabricmc.loader.api.Version;
import net.fabricmc.loader.api.metadata.version.VersionPredicate;

/** Usa el parser del Loader fijado; no arranca Minecraft. */
public class FabricVersions {
    public static void main(String[] args) throws Exception {
        var reader = new BufferedReader(new InputStreamReader(System.in));
        String line;
        while ((line = reader.readLine()) != null) {
            String[] parts = line.split("\t", -1);
            if (parts[0].equals("match")) {
                System.out.println(VersionPredicate.parse(parts[2]).test(Version.parse(parts[1])));
            } else if (parts[0].equals("compare")) {
                System.out.println(Version.parse(parts[1]).compareTo(Version.parse(parts[2])));
            } else {
                throw new IllegalArgumentException("Operación desconocida");
            }
        }
    }
}
